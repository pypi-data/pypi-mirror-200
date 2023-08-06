import numpy as np
from flgo.utils import fmodule
import copy
import flgo.system_simulator.base as ss
import math
import collections
import torch.multiprocessing as mp
import torch

class BasicParty:
    def __init__(self, *args, **kwargs):
        self.actions = {}
        self.id = None

    def register_action_to_mtype(self, action_name: str, mtype):
        """
        Register an existing instance method as the action to the message type.
        Args:
            action_name: the name of the instance method
            mtype: the message type
        """
        if action_name not in self.__dict__.keys():
            raise NotImplementedError("There is no method named `{}` in the class instance.".format(action_name))
        self.actions[mtype] = self.__dict__[action_name]

    def message_handler(self, package):
        """
        Handling the received message by excuting the corresponding action.
        Args:
            package: the package received from other parties (i.e. the content of the message)
            mtype: the message type
        Returns:
            action_reult
        """
        try:
            mtype = package['__mtype__']
        except:
            raise KeyError("__mtype__ must be a key of the package")
        if mtype not in self.actions.keys():
            raise NotImplementedError("There is no action corresponding to message type {}.".format(mtype))
        return self.actions[mtype](package)

    def set_data(self, data, flag='train') -> None:
        setattr(self, flag+'_data', data)
        if flag=='train':
            self.datavol = len(data)
            if hasattr(self, 'batch_size'):
                # reset batch_size
                if self.batch_size<0: self.batch_size = len(self.train_data)
                elif self.batch_size>=1: self.batch_size = int(self.batch_size)
                else: self.batch_size = int(self.datavol * self.batch_size)
            # reset num_steps
            if hasattr(self, 'num_steps') and hasattr(self, 'num_epochs'):
                if self.num_steps > 0:
                    self.num_epochs = 1.0 * self.num_steps/(math.ceil(self.datavol / self.batch_size))
                else:
                    self.num_steps = self.num_epochs * math.ceil(self.datavol / self.batch_size)

    def register_parties(self, parties):
        # set the accessible parties
        self.parties = parties

    def communicate_with(self, target_id, package={}):
        """
        Pack the information that is needed for client_id to improve the global model
        Args:
            client_id (int): the id of the client to communicate with
            package (dict): the package to be sended to the client
            mtype (anytype): the type of the message that is used to decide the action of the client
        Returns:
            client_package (dict): the reply from the client and will be 'None' if losing connection
        """
        return self.gv.communicator.request(self.id, target_id, package)

    def initialize(self, *args, **kwargs):
        return

class BasicServer(BasicParty):
    def __init__(self, option={}):
        super().__init__()
        self.test_data=None
        self.valid_data = None
        self.train_data = None
        self.model = None
        # basic configuration
        self.task = option['task']
        self.eval_interval = option['eval_interval']
        self.num_parallels= option['num_parallels']
        # server calculator
        self.device = self.gv.apply_for_device() if not option['server_with_cpu'] else torch.device('cpu')
        self.calculator = self.gv.TaskCalculator(self.device, optimizer_name = option['optimizer'])
        # hyper-parameters during training process
        self.num_rounds = option['num_rounds']
        self.num_steps = option['num_steps']
        self.num_epochs = option['num_epochs']
        self.proportion = option['proportion']
        self.decay_rate = option['learning_rate_decay']
        self.lr_scheduler_type = option['lr_scheduler']
        self.lr = option['learning_rate']
        self.sample_option = option['sample']
        self.aggregation_option = option['aggregate']
        # systemic option
        self.tolerance_for_latency = 999999
        # algorithm-dependent parameters
        self.algo_para = {}
        self.current_round = 1
        # all options
        self.option = option
        self.id = -1

    def run(self):
        """
        Start the federated learning symtem where the global model is trained iteratively.
        """
        self.gv.logger.time_start('Total Time Cost')
        self.gv.logger.info("--------------Initial Evaluation--------------")
        self.gv.logger.time_start('Eval Time Cost')
        self.gv.logger.log_once()
        self.gv.logger.time_end('Eval Time Cost')
        while self.current_round <= self.num_rounds:
            self.gv.clock.step()
            # iterate
            self.gv.logger.time_start('Iterate Time Cost')
            updated = self.iterate()
            self.gv.logger.time_end('Iterate Time Cost')
            # using logger to evaluate the model if the model is updated
            if updated is True or updated is None:
                self.gv.logger.info("--------------Round {}--------------".format(self.current_round))
                # check log interval
                if self.gv.logger.check_if_log(self.current_round, self.eval_interval):
                    self.gv.logger.time_start('Eval Time Cost')
                    self.gv.logger.log_once()
                    self.gv.logger.time_end('Eval Time Cost')
                # check if early stopping
                if self.gv.logger.early_stop(): break
                self.current_round += 1
            # decay learning rate
            self.global_lr_scheduler(self.current_round)
        self.gv.logger.info("=================End==================")
        self.gv.logger.time_end('Total Time Cost')
        # save results as .json file
        self.gv.logger.save_output_as_json()
        return

    def iterate(self):
        """
        The standard iteration of each federated round that contains three
        necessary procedure in FL: client selection, communication and model aggregation.
        Args:
        Returns:
        """
        # sample clients: MD sampling as default
        self.selected_clients = self.sample()
        # training
        models = self.communicate(self.selected_clients)['model']
        # aggregate: pk = 1/K as default where K=len(selected_clients)
        self.model = self.aggregate(models)
        return len(models)>0

    @ss.with_dropout
    @ss.with_clock
    def communicate(self, selected_clients, mtype=0, asynchronous=False):
        """
        The whole simulating communication procedure with the selected clients.
        This part supports for simulating the client dropping out.
        Args:
            selected_clients (list of int): the clients to communicate with
            mtype (anytype): type of message
            asynchronous (bool): asynchronous communciation or synchronous communcation
        Returns:
            :the unpacked response from clients that is created ny self.unpack()
        """
        packages_received_from_clients = []
        received_package_buffer = {}
        communicate_clients = list(set(selected_clients))
        # prepare packages for clients
        for cid in communicate_clients:
            received_package_buffer[cid] = None
        # try:
        #     for cid in communicate_clients:
        #         self.sending_package_buffer[cid] = self.pack(cid, mtype)
        #         self.sending_package_buffer[cid]['__mtype__'] = mtype
        # except Exception as e:
        #     if str(self.device) != 'cpu':
        #         self.model.to(torch.device('cpu'))
        #         for cid in communicate_clients:
        #             self.sending_package_buffer[cid] = self.pack(cid, mtype)
        #             self.sending_package_buffer[cid]['__mtype__'] = mtype
        #         self.model.to(self.device)
        #     else:
        #         raise e
        # communicate with selected clients
        if self.num_parallels <= 1:
            # computing iteratively
            for client_id in communicate_clients:
                server_pkg = self.pack(cid, mtype)
                server_pkg['__mtype__'] = mtype
                response_from_client_id = self.communicate_with(client_id, package=server_pkg)
                packages_received_from_clients.append(response_from_client_id)
        else:
            # computing in parallel with torch.multiprocessing
            pool = mp.Pool(self.num_parallels)
            for client_id in communicate_clients:
                server_pkg = self.pack(cid, mtype)
                server_pkg['__mtype__'] = mtype
                self.clients[client_id].update_device(self.gv.apply_for_device())
                args = (int(client_id), server_pkg)
                packages_received_from_clients.append(pool.apply_async(self.communicate_with, args=args))
            pool.close()
            pool.join()
            packages_received_from_clients = list(map(lambda x: x.get(), packages_received_from_clients))
        for i,cid in enumerate(communicate_clients): received_package_buffer[cid] = packages_received_from_clients[i]
        packages_received_from_clients = [received_package_buffer[cid] for cid in selected_clients if received_package_buffer[cid]]
        self.received_clients = selected_clients
        return self.unpack(packages_received_from_clients)
    
    @ss.with_latency
    def communicate_with(self, target_id, package={}):
        return super(BasicServer, self).communicate_with(target_id, package)
    
    
    def pack(self, client_id, mtype=0, *args, **kwargs):
        """
        Pack the necessary information for the client's local training.
        Any operations of compression or encryption should be done here.
        Args:
            client_id (int): the id of the client to communicate with
        Returns:
            a dict that only contains the global model as default.
        """
        return {
            "model" : copy.deepcopy(self.model),
        }

    def unpack(self, packages_received_from_clients):
        """
        Unpack the information from the received packages. Return models and losses as default.
        Args:
            packages_received_from_clients (list of dict):
        Returns::
            res (dict): collections.defaultdict that contains several lists of the clients' reply
        """
        if len(packages_received_from_clients)==0: return collections.defaultdict(list)
        res = {pname:[] for pname in packages_received_from_clients[0]}
        for cpkg in packages_received_from_clients:
            for pname, pval in cpkg.items():
                res[pname].append(pval)
        return res

    def global_lr_scheduler(self, current_round):
        """
        Control the step size (i.e. learning rate) of local training
        Args:
            current_round (int): the current communication round
        """
        if self.lr_scheduler_type == -1:
            return
        elif self.lr_scheduler_type == 0:
            """eta_{round+1} = DecayRate * eta_{round}"""
            self.lr*=self.decay_rate
            for c in self.clients:
                c.set_learning_rate(self.lr)
        elif self.lr_scheduler_type == 1:
            """eta_{round+1} = eta_0/(round+1)"""
            self.lr = self.option['learning_rate']*1.0/(current_round+1)
            for c in self.clients:
                c.set_learning_rate(self.lr)

    @ss.with_availability
    def sample(self):
        """Sample the clients.
        Args:
        Returns:
            a list of the ids of the selected clients
        """
        all_clients = self.available_clients if 'available' in self.sample_option else [cid for cid in range(self.num_clients)]
        # full sampling with unlimited communication resources of the server
        if 'full' in self.sample_option:
            return all_clients
        # sample clients
        elif 'uniform' in self.sample_option:
            # original sample proposed by fedavg
            selected_clients = list(np.random.choice(all_clients, min(self.clients_per_round, len(all_clients)), replace=False)) if len(all_clients)>0 else []
        elif 'md' in self.sample_option:
            # the default setting that is introduced by FedProx, where the clients are sampled with the probability in proportion to their local data sizes
            local_data_vols = [self.clients[cid].datavol for cid in all_clients]
            total_data_vol = sum(local_data_vols)
            p = np.array(local_data_vols)/total_data_vol
            selected_clients = list(np.random.choice(all_clients, self.clients_per_round, replace=True, p=p)) if len(all_clients)>0 else []
        return selected_clients

    def aggregate(self, models: list, *args, **kwargs):
        """
        Aggregate the locally improved models.
        Args:
            models (list): a list of local models
        Returns:
            the averaged result
        pk = nk/n where n=self.data_vol
        K = |S_t|
        N = |S|
        -------------------------------------------------------------------------------------------------------------------------
         weighted_scale                 |uniform (default)          |weighted_com (original fedavg)   |other
        ==========================================================================================================================
        N/K * Σpk * model_k             |1/K * Σmodel_k             |(1-Σpk) * w_old + Σpk * model_k  |Σ(pk/Σpk) * model_k
        """
        if len(models) == 0: return self.model
        local_data_vols = [c.datavol for c in self.clients]
        total_data_vol = sum(local_data_vols)
        if self.aggregation_option == 'weighted_scale':
            p = [1.0 * local_data_vols[cid] /total_data_vol for cid in self.received_clients]
            K = len(models)
            N = self.num_clients
            return fmodule._model_sum([model_k * pk for model_k, pk in zip(models, p)]) * N / K
        elif self.aggregation_option == 'uniform':
            return fmodule._model_average(models)
        elif self.aggregation_option == 'weighted_com':
            p = [1.0 * local_data_vols[cid] / total_data_vol for cid in self.received_clients]
            w = fmodule._model_sum([model_k * pk for model_k, pk in zip(models, p)])
            return (1.0-sum(p))*self.model + w
        else:
            p = [1.0 * local_data_vols[cid] / total_data_vol for cid in self.received_clients]
            sump = sum(p)
            p = [pk/sump for pk in p]
            return fmodule._model_sum([model_k * pk for model_k, pk in zip(models, p)])

    def global_test(self, flag='valid'):
        """
        Validate accuracies and losses on clients' local datasets
        Args:
            dataflag (str): choose train data or valid data to evaluate
        Returns:
            metrics (dict): a dict contains the lists of each metric_value of the clients
        """
        all_metrics = collections.defaultdict(list)
        for c in self.clients:
            client_metrics = c.test(self.model, flag)
            for met_name, met_val in client_metrics.items():
                all_metrics[met_name].append(met_val)
        return all_metrics

    def test(self, model=None, flag='test'):
        """
        Evaluate the model on the test dataset owned by the server.
        Args:
            model (flgo.utils.fmodule.FModule): the model need to be evaluated
        Returns::
            metrics (dict): specified by the task during running time (e.g. metric = [mean_accuracy, mean_loss] when the task is classification)
        """
        if model is None: model=self.model
        if flag == 'valid': dataset = self.valid_data
        elif flag == 'test': dataset = self.test_data
        else: dataset = self.train_data
        if dataset is None: return {}
        else:
            return self.calculator.test(model, dataset, batch_size = self.option['test_batch_size'], num_workers = self.option['num_workers'], pin_memory = self.option['pin_memory'])

    def init_algo_para(self, algo_para: dict):
        """
        Initialize the algorithm-dependent hyper-parameters for the server and all the clients.
        Args:
            algo_paras (dict): the dict that defines the hyper-parameters (i.e. name, value and type) for the algorithm.

        Example 1:
            calling `self.init_algo_para({'u':0.1})` will set the attributions `server.u` and `c.u` as 0.1 with type float where `c` is an instance of `CLient`.
        Note:
            Once `option['algo_para']` is not `None`, the value of the pre-defined hyperparameters will be replaced by the list of values in `option['algo_para']`,
            which requires the length of `option['algo_para']` is equal to the length of `algo_paras`
        """
        self.algo_para = algo_para
        if len(self.algo_para)==0: return
        # initialize algorithm-dependent hyperparameters from the input options
        if self.option['algo_para'] is not None:
            # assert len(self.algo_para) == len(self.option['algo_para'])
            keys = list(self.algo_para.keys())
            for i,pv in enumerate(self.option['algo_para']):
                if i==len(self.option['algo_para']): break
                para_name = keys[i]
                try:
                    self.algo_para[para_name] = type(self.algo_para[para_name])(pv)
                except:
                    self.algo_para[para_name] = pv
        # register the algorithm-dependent hyperparameters as the attributes of the server and all the clients
        for para_name, value in self.algo_para.items():
            self.__setattr__(para_name, value)
            for c in self.clients:
                c.__setattr__(para_name, value)
        return

    def get_tolerance_for_latency(self):
        return self.tolerance_for_latency

    def wait_time(self, t=1):
        ss.clock.step(t)
        return

    @property
    def available_clients(self):
        """
        Return all the available clients at current round.
        Args:
        Returns:: a list of indices of currently available clients
        """
        return [cid for cid in range(self.num_clients) if self.clients[cid].is_idle()]

    def register_clients(self, clients):
        """
        register self.clients=clients
        Args:
            clients (list of Client()): clients
        Returns:: a list of indices of currently available clients
        """
        self.clients = clients
        self.num_clients = len(clients)
        for cid, c in enumerate(self.clients):
            c.client_id = cid
        for c in self.clients:c.register_server(self)
        self.clients_per_round = max(int(self.num_clients * self.proportion), 1)
        self.selected_clients = []
        self.dropped_clients = []

class BasicClient(BasicParty):
    def __init__(self, option={}):
        super().__init__()
        self.id = None
        # create local dataset
        self.data_loader = None
        self.test_data=None
        self.valid_data = None
        self.train_data = None
        self.model = None
        # local calculator
        self.device = self.gv.apply_for_device()
        self.calculator = self.gv.TaskCalculator(self.device, option['optimizer'])
        # hyper-parameters for training
        self.optimizer_name = option['optimizer']
        self.learning_rate = option['learning_rate']
        self.momentum = option['momentum']
        self.weight_decay = option['weight_decay']
        self.batch_size = option['batch_size']
        self.num_steps = option['num_steps']
        self.num_epochs = option['num_epochs']
        self.model = None
        self.test_batch_size = option['test_batch_size']
        self.loader_num_workers = option['num_workers']
        self.current_steps = 0
        # system setting
        self._effective_num_steps = self.num_steps
        self._latency = 0
        # server
        self.server = None
        # actions of different message type
        self.option = option
        self.actions = {0: self.reply}

    def initialize(self):
        # to be implemented for customized initializing operations
        return

    @ss.with_completeness
    @fmodule.with_multi_gpus
    def train(self, model):
        """
        Standard local training procedure. Train the transmitted model with local training dataset.
        Args:
            model (FModule): the global model
        Returns:
        """
        model.train()
        optimizer = self.calculator.get_optimizer(model, lr=self.learning_rate, weight_decay=self.weight_decay, momentum=self.momentum)
        for iter in range(self.num_steps):
            # get a batch of data
            batch_data = self.get_batch_data()
            model.zero_grad()
            # calculate the loss of the model on batched dataset through task-specified calculator
            loss = self.calculator.compute_loss(model, batch_data)['loss']
            loss.backward()
            optimizer.step()
        return

    @ fmodule.with_multi_gpus
    def test(self, model, flag='valid'):
        """
        Evaluate the model with local data (e.g. training data or validating data).
        Args:
            model (FModule):
            dataflag (str): choose the dataset to be evaluated on
        Returns:
            metric (dict): specified by the task during running time (e.g. metric = [mean_accuracy, mean_loss] when the task is classification)
        """
        if flag == 'valid': dataset = self.valid_data
        elif flag == 'test': dataset = self.test_data
        else: dataset = self.train_data
        if dataset is not None:
            return self.calculator.test(model, dataset, self.test_batch_size, self.option['num_workers'])
        else:
            return {}

    def unpack(self, received_pkg):
        """
        Unpack the package received from the server
        Args:
            received_pkg (dict): a dict contains the global model as default
        Returns:
            the unpacked information that can be rewritten
        """
        # unpack the received package
        return received_pkg['model']

    def reply(self, svr_pkg):
        """
        Reply to server with the transmitted package.
        The whole local procedure should be planned here.
        The standard form consists of three procedure:
        unpacking the server_package to obtain the global model,
        training the global model, and finally packing the updated
        model into client_package.
        Args:
            svr_pkg (dict): the package received from the server
        Returns:
            client_pkg (dict): the package to be send to the server
        """
        model = self.unpack(svr_pkg)
        self.train(model)
        cpkg = self.pack(model)
        return cpkg

    def pack(self, model, *args, **kwargs):
        """
        Packing the package to be send to the server. The operations of compression
        of encryption of the package should be done here.
        Args:
            model: the locally trained model
        Returns
            package: a dict that contains the necessary information for the server
        """
        return {
            "model" : model,
        }

    def is_idle(self):
        """
        Check if the client is active to participate training.
        Args:
        Returns:
            True if the client is active according to the active_rate else False
        """
        return self.gv.simulator.client_states[self.id]=='idle'

    def is_dropped(self):
        """
        Check if the client drops out during communicating.
        Args:
        Returns:
            True if the client was being dropped
        """
        return self.gv.simulator.client_states[self.id]=='dropped'

    def is_working(self):
        return self.gv.simulator.client_states[self.id]=='working'

    def train_loss(self, model):
        """
        Get the task specified loss of the model on local training data
        Args: model:
        Returns:
        """
        return self.test(model,'train')['loss']

    def valid_loss(self, model):
        """
        Get the task specified loss of the model on local validating data
        Args: model:
        Returns:
        """
        return self.test(model)['loss']

    def set_model(self, model):
        """
        set self.model
        Args: model:
        Returns:
        """
        self.model = model

    def register_server(self, server=None):
        if server is not None:
            self.server = server

    def set_local_epochs(self, epochs=None):
        if epochs is None: return
        self.epochs = epochs
        self.num_steps = self.epochs * math.ceil(len(self.train_data)/self.batch_size)
        return

    def set_batch_size(self, batch_size=None):
        if batch_size is None: return
        self.batch_size = batch_size

    def set_learning_rate(self, lr = None):
        """
        set the learning rate of local training
        Args: lr:
        Returns:
        """
        self.learning_rate = lr if lr else self.learning_rate

    def get_time_response(self):
        """
        Get the latency amount of the client
        Returns: self.latency_amount if client not dropping out
        """
        return np.inf if self.dropped else self.time_response

    def get_batch_data(self):
        """
        Get the batch of data
        Returns:
            a batch of data
        """
        try:
            batch_data = next(self.data_loader)
        except Exception as e:
            self.data_loader = iter(self.calculator.get_dataloader(self.train_data, batch_size=self.batch_size, num_workers=self.loader_num_workers, pin_memory=self.option['pin_memory']))
            batch_data = next(self.data_loader)
        # clear local DataLoader when finishing local training
        self.current_steps = (self.current_steps+1) % self.num_steps
        if self.current_steps == 0:self.data_loader = None
        return batch_data

    def update_device(self, dev):
        """
        Update running-time GPU device to the inputted dev, including change the client's device and the task_calculator's device
        Args:
            dev (torch.device): target dev
        Returns:
        """
        self.device = dev
        self.calculator = self.gv.TaskCalculator(dev, self.calculator.optimizer_name)
