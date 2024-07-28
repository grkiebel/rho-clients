from threading import Thread
from time import sleep
from typing import List
from ..api import g_api as apx
from ..log_config import get_logger

logger = get_logger("WorkMgr")


class WorkMgr:
    def __init__(self, interval: int = 8) -> None:
        self.interval = interval
        self.task_creates: List[apx.TaskCreate] = []
        self.thread: Thread = None

    def run(self):
        self.thread = Thread(target=self.run_archive_monitor)

    def run_archive_monitor(self):
        while True:
            sleep(self.interval)
            archived_work = apx.archive_list()
            ids = [str(archive.work_id) for archive in archived_work]
            recent = ids[-3:]
            logger.info(f"Archived work: Num: {len(ids)} ,{', '.join(recent)}")
            # TODO: print archived work iteam and delete it
