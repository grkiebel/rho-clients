from time import sleep
from typing import List
from threading import Thread
from access import api_access as api_axs
from access import (
    MatchCheckerBase,
    WorkFinder,
    TaskCreateRep,
    ToolCreateRep,
    WorkCreateRep,
    verify_service_status,
)
from app_models import AppMatchChecker
from sims import ToolWorker, SimTool, SimTask


def clear_db():
    outcome = api_axs.delete_all_tools()
    print(outcome)
    outcome = api_axs.delete_all_tasks()
    print(outcome)
    outcome = api_axs.delete_all_reports()
    print(outcome)
    outcome = api_axs.delete_all_work()
    print(outcome)
    outcome = api_axs.delete_all_archived_work()
    print(outcome)


def make_tool(tool: SimTool):
    tool_create_rep = ToolCreateRep(tool_id=tool.tool_id, tool_skills=tool.tool_skills)
    outcome = api_axs.create_tool(tool_create_rep)
    print(outcome)


def make_task(task: SimTask) -> None:
    task_create_rep = TaskCreateRep(task_id=task.task_id, task_needs=task.task_needs)
    outcome = api_axs.create_task(task_create_rep)
    print(outcome)


def assign_work() -> None:
    work_finder = WorkFinder(
        match_checker=AppMatchChecker()
    )  # just use MatchCheckerBase for "match all"
    for tool_id, task_id in work_finder.pairs:
        work_create_rep = WorkCreateRep(tool_id=tool_id, task_id=task_id)
        outcome = api_axs.create_work(work_create_rep)
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
        archived_work = api_axs.get_all_archived_work()
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
        self.sim_tools: List[SimTool] = [SimTool() for _ in range(num_tools)]
        self.sim_tasks: List[SimTask] = [SimTask() for _ in range(num_tasks)]
        self.threads: List[Thread] = []

    def run(self):
        clear_db()

        for tool in self.sim_tools:
            make_tool(tool)

        for SimTask in self.sim_tasks:
            make_task(SimTask)

        thread = run_assigner_in_thread()
        self.threads.append(thread)

        for tool in self.sim_tools:
            thread = run_tool_in_thread(tool.tool_id)
            self.threads.append(thread)

        thread = run_archive_monitor_in_thread()
        self.threads.append(thread)


if __name__ == "__main__":

    if not verify_service_status():
        exit()

    SimRun(num_tasks=20, num_tools=10).run()

    print("done")
