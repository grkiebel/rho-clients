from time import sleep
from typing import List
from threading import Thread
from rho_clients.log_config import get_logger
from rho_clients.api import g_api as apx
from rho_clients.client_apps import app_models as cam
from rho_clients.client_apps.assigner_app import WorkFinder
from rho_clients.client_apps.tool_app import ToolWorker
from rho_clients.cmds import y_sim as sim


apx.initialize("http://localhost:8080", get_logger("API-Access"))


def clear_db():
    outcome = apx.delete_all_tools()
    print(outcome)
    outcome = apx.delete_all_tasks()
    print(outcome)
    outcome = apx.delete_all_reports()
    print(outcome)
    outcome = apx.delete_all_work()
    print(outcome)
    outcome = apx.delete_all_archived_work()
    print(outcome)


# def make_tool(tool: SimTool):
#     tool_create_rep = apx.ToolCreate(tool_id=tool.tool_id, tool_skills=tool.tool_skills)
#     outcome = apx.create_tool(tool_create_rep)
#     print(outcome)


# def make_task(task: SimTask) -> None:
#     task_create_rep = apx.TaskCreate(task_id=task.task_id, task_needs=task.task_needs)
#     outcome = apx.create_task(task_create_rep)
#     print(outcome)


def assign_work() -> None:
    work_finder = cam.WorkFinder(
        match_checker=cam.AppMatchChecker()
    )  # just use MatchCheckerBase for "match all"
    for tool_id, task_id in work_finder.pairs:
        work_create_rep = apx.WorkCreate(tool_id=tool_id, task_id=task_id)
        outcome = apx.create_work(work_create_rep)
        print(outcome.message)


def run_assigner():
    while True:
        assign_work()
        sleep(8)


def run_tool_in_thread(tool_id) -> Thread:
    tool_worker = ToolWorker(tool_id)
    thread = Thread(target=tool_worker.run)
    thread.start()
    return thread


def run_assigner_in_thread() -> Thread:
    thread = Thread(target=run_assigner)
    thread.start()
    return thread


def run_archive_monitor():
    while True:
        archived_work = apx.get_all_archived_work()
        ids = [str(archive.work_id) for archive in archived_work]
        recent = ids[-3:]
        print(f"Archived work: Num: {len(ids)} ,{', '.join(recent)}")
        # TODO: print archived work item and delete it
        sleep(10)


def run_archive_monitor_in_thread():
    thread = Thread(target=run_archive_monitor)
    thread.start()
    return thread


class SimRun:

    def __init__(self, num_tools: int = 5, num_tasks: int = 10):
        self.tool_creates: List[apx.ToolCreate] = sim.make_tool_create_list(num_tools)
        self.task_creates: List[apx.TaskCreate] = sim.make_task_create_list(num_tasks)

        self.threads: List[Thread] = []

    def run(self):
        clear_db()

        for tool_create in self.tool_creates:
            apx.tool_create(tool_create)

        for task_create in self.task_creates:
            apx.task_create(task_create)

        thread = run_assigner_in_thread()
        self.threads.append(thread)

        for tool_create in self.tool_creates:
            thread = run_tool_in_thread(tool_create.tool_id)
            self.threads.append(thread)

        thread = run_archive_monitor_in_thread()
        self.threads.append(thread)


if __name__ == "__main__":

    status = apx.general_status()
    print(status)

    SimRun(num_tasks=20, num_tools=10).run()

    print("done")
