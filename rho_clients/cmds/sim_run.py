import argparse
from time import sleep
from typing import List
from threading import Thread
from ..log_config import get_logger
from ..api import g_api as apx
from ..client_apps import tool_app as tap
from . import cmd_helpers as hp

""" This module runs a full scale simulated operation 
of the various rho-service clients. """

rnd_int = hp.random_int_generator(0, 3)


def assign_work() -> None:
    work_create_list = hp.make_work_create_list(num_work_items=50)
    for work_create in work_create_list:
        outcome = apx.work_create(work_create)
        print(outcome.message)


def run_assigner():
    while True:
        assign_work()
        sleep(8)


def run_tool_in_thread(tool_id) -> Thread:
    thread = Thread(target=tap.simulate_work, kwargs={"tool_id": tool_id})
    thread.start()
    return thread


def run_assigner_in_thread() -> Thread:
    thread = Thread(target=run_assigner)
    thread.start()
    return thread


def run_archive_monitor():
    while True:
        archived_work = apx.archive_list()
        ids = [str(archive.work_id) for archive in archived_work]
        recent = ids[-3:]
        print(f"Archived work: Num: {len(ids)} ,{', '.join(recent)}")
        # TODO: print archived work iteam and delete it
        sleep(10)


def run_archive_monitor_in_thread():
    thread = Thread(target=run_archive_monitor)
    thread.start()
    return thread


class SimRun:
    """This class runs a full scale simulated operation"""

    def __init__(self, num_tools: int = 10, num_tasks: int = 20):
        self.num_tools = num_tools
        self.num_tasks = num_tasks
        self.tool_creates: List[apx.ToolCreate] = []
        self.task_creates: List[apx.TaskCreate] = []

        self.threads: List[Thread] = []

    def run(self):
        hp.clear_db()

        for _ in range(self.num_tools):
            tool_create = hp.make_tool_create()
            self.tool_creates.append(tool_create)
            apx.tool_create(tool_create)
            print(f"Tool created: {tool_create.tool_id}")
            sleep(next(rnd_int))

        for _ in range(self.num_tasks):
            task_create = hp.make_task_create()
            self.task_creates.append(task_create)
            apx.task_create(task_create)
            print(f"Task created: {task_create.task_id}")
            sleep(next(rnd_int))

        for tool_create in self.tool_creates:
            thread = run_tool_in_thread(tool_create.tool_id)
            print(f"Tool running: {tool_create.tool_id}")
            self.threads.append(thread)

        sleep(5)

        thread = run_assigner_in_thread()
        print("Assigner running")
        self.threads.append(thread)

        thread = run_archive_monitor_in_thread()
        self.threads.append(thread)


def main():
    args = get_args()
    apx.initialize(args.rho_service_url, get_logger("API-Access"))
    SimRun(num_tasks=args.num_tasks, num_tools=args.num_tools).run()


def get_args():
    parser = argparse.ArgumentParser(description="API Generator")
    parser.add_argument(
        "-url",
        "--rho_service_url",
        help="URL to the rho-service",
        default="http://localhost:8080",
    )
    parser.add_argument(
        "-tls",
        "--num_tools",
        help="Number of tools to create",
        default=10,
    )
    parser.add_argument(
        "-tks",
        "--num_tasks",
        help="Number of tasks to create",
        default=20,
    )
    args = parser.parse_args()
    return args
