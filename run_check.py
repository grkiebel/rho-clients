from time import sleep
from typing import List
from threading import Thread
from rho_clients.log_config import get_logger
from rho_clients.api import g_api as apx
from rho_clients.client_apps import app_models as cam
from rho_clients.client_apps.assigner_app import find_assignments
from rho_clients.client_apps import tool_app as tap
from rho_clients.cmds import helpers as hp


apx.initialize("http://localhost:8080", get_logger("API-Access"))


def clear_db():
    outcome = apx.tool_clear()
    print(outcome)
    outcome = apx.task_clear()
    print(outcome)
    outcome = apx.report_clear()
    print(outcome)
    outcome = apx.work_clear()
    print(outcome)
    outcome = apx.archive_clear()
    print(outcome)


def assign_work() -> None:
    pairs = find_assignments(cam.AppMatchChecker())
    for tool_id, task_id in pairs:
        work_create_rep = apx.WorkCreate(tool_id=tool_id, task_id=task_id)
        outcome = apx.work_create(work_create_rep)
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

    def __init__(self, num_tools: int = 5, num_tasks: int = 10):
        self.num_tools = num_tools
        self.num_tasks = num_tasks
        self.tool_creates: List[apx.ToolCreate] = []
        self.task_creates: List[apx.TaskCreate] = []

        self.threads: List[Thread] = []

    def run(self):
        clear_db()

        for _ in range(self.num_tools):
            tool_create = hp.make_tool_create()
            self.tool_creates.append(tool_create)
            apx.tool_create(tool_create)
            print(f"Tool created: {tool_create.tool_id}")
            hp.random_delay()

        for _ in range(self.num_tasks):
            task_create = hp.make_task_create()
            self.task_creates.append(task_create)
            apx.task_create(task_create)
            print(f"Task created: {task_create.task_id}")
            hp.random_delay()

        for tool_create in self.tool_creates:
            thread = run_tool_in_thread(tool_create.tool_id)
            print(f"Tool running: {tool_create.tool_id}")
            self.threads.append(thread)

        hp.random_delay()

        thread = run_assigner_in_thread()
        print("Assigner running")
        self.threads.append(thread)

        thread = run_archive_monitor_in_thread()
        self.threads.append(thread)


if __name__ == "__main__":

    status = apx.general_status()
    print(status)

    SimRun(num_tasks=20, num_tools=10).run()

    print("done")
