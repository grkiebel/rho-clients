import os
from time import sleep
from ..generated import api_access as apx
from ..log_config import get_logger


logger = get_logger("Tool")


def interval_gen(base: int = 15, max: int = 300, step: int = 20):
    current_value = base
    while True:
        yield current_value
        inc = step if current_value < max else 0
        current_value += inc


class WorkContext:

    def __init__(self, tool_base: object):
        self.work_id: int = None
        self.tool_id: str = None
        self.task_id: str = None
        self.tool_skills: dict = None
        self.task_needs: dict = None
        self.send_report: callable = None
        self.send_successful: callable = None
        self.send_failed: callable = None
        self.logger = logger
        self.load(tool_base)

    def set(self, work: apx.WorkInfo):
        self.work_id = work.work_id
        self.job_id = work.tool_id
        self.task_id = work.task_id
        self.tool_skills = work.tool_skills
        self.task_needs = work.task_needs

    def clear(self):
        self.work_id = None
        self.job_id = None
        self.task_id = None
        self.tool_skills = None
        self.task_needs = None

    def load(self, obj: object):
        callables = [
            attr
            for attr in dir(obj)
            if callable(getattr(obj, attr)) and not attr.startswith("_")
        ]
        for c in callables:
            if hasattr(self, c):
                setattr(self, c, getattr(obj, c))


class ToolBase:
    def __init__(self, tool_id: str):
        self.tool_id: str = tool_id
        self.work_context = WorkContext(self)

    def run(self, do_work: callable):
        self.logger = get_logger(self.tool_id)
        self.logger.info(f"Starting tool with id {self.tool_id}")
        while True:
            self.work_context.clear()
            self.ready_for_work()
            self.get_work()
            if not do_work(self.work_context):
                break

    def ready_for_work(self):
        interval = interval_gen()
        while True:
            outcome: apx.Outcome = apx.mark_tool_as_ready_for_work(self.tool_id)
            self.logger.info(outcome)
            if outcome.success:
                return
            wait = next(interval)
            self.logger.info(
                f"Waiting {wait} seconds to check for tool to be unassigned"
            )
            sleep(wait)

    def get_work(self):
        interval = interval_gen()
        while True:
            work: apx.WorkInfo = apx.get_work_assigned_to_the_specified_tool(
                self.tool_id
            )
            if not work.work_id:
                wait = next(interval)
                self.logger.info(f"Waiting {wait} seconds to check for assigned work")
                sleep(wait)
            else:
                self.work_context.set(work)
                return

    def send_report(self, work_id: str, status: str, details: dict):
        report_create_rep = apx.ReportCreate(status=status, details=details)
        apx.add_a_report_to_a_work_item(work_id, report_create_rep)
        self.logger.info(f"Report sent for {work_id} with status {status}")

    def send_successful(self, work_id: str, details: dict):
        report_create_rep = apx.add_a_report_to_a_work_item(
            status="success", details=details
        )
        apx.mark_work_as_completed_and_successful(work_id, report_create_rep)
        self.logger.info(f"Successful completion sent for work item {work_id}")

    def send_failed(self, work_id: str, details: dict):
        report_create_rep = apx.ReportCreate(status="failed", details=details)
        apx.mark_work_as_completed_and_failed(work_id, report_create_rep)
        self.logger.info(f"Failed completion sent for work item {work_id}")


def get_tool_id() -> str:
    tool_id = os.environ.get("TOOL_ID")
    if not tool_id:
        print("TOOL_ID environment variable not set.")
        exit(1)
    logger.info(f"Starting tool with id {tool_id}")
    return tool_id
