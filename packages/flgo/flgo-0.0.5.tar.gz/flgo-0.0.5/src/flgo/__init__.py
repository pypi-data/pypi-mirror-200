from .utils.fflow import init, gen_task_by_config, gen_task_by_para, tune, run_in_parallel, multi_init_and_run

gen_task = gen_task_by_config
communicator = None

class VirtualCommunicator:
    def __init__(self, objects):
        self.objects = objects

    def request(self, source, target, package):
        # send package to the target object with `package` and `mtype`, and then listen from it
        return self.objects[target+1].message_handler(package)
