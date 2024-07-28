from threading import Thread
from time import sleep
from ..api import g_api as apx
from ..cmds import cmd_helpers as hp
from ..log_config import get_logger

logger = get_logger("AssignerMgr")


class AssignerMgr:
    """This class runs an assigner in a separate thread.
    In this case, the assigner is implemented by the exaple assigner.
    In a real-world scenario, the assigner could be implemented by an external system.
    """

    def run(self, interval: int = 8):
        self.interval = interval
        self.run_assigner_in_thread()

    def run_assigner_in_thread(self) -> Thread:
        thread = Thread(target=self.run_assigner)
        thread.start()
        return thread

    def run_assigner(self):
        while True:
            self.assign_work()
            sleep(self.interval)

    def assign_work(self) -> None:
        work_create_list = hp.make_work_create_list(num_work_items=50)
        for work_create in work_create_list:
            outcome = apx.work_create(work_create)
            logger.info(outcome.message)
