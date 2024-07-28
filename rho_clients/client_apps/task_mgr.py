from threading import Thread
from time import sleep
from typing import List
from ..api import g_api as apx
from ..cmds import cmd_helpers as hp
from ..log_config import get_logger


rnd_int = hp.random_int_generator(0, 3)

logger = get_logger("TaskMgr")

""" This module simulates the creation of tasks.  
In a real-world scenario, would likely originate from an external system.
"""


class TaskMgr:
    """This class creates new tasks up to given number"""

    def __init__(self, num_tasks: int = 30) -> None:
        self.num_tasks = num_tasks
        self.task_creates: List[apx.TaskCreate] = []
        self.thread: Thread = None

    def run(self):
        self.thread = self.generate_tasks()

    def generate_tasks(self):
        for _ in range(self.num_tasks):
            task_create = hp.make_task_create()
            self.task_creates.append(task_create)
            apx.task_create(task_create)
            logger.info(f"Task created: {task_create.task_id}")
            sleep(next(rnd_int))


# create tasks
# remove work info for tasks
# check for wallflowers
