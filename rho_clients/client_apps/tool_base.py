import os
from time import sleep
from ..api import g_api as apx
from ..log_config import get_logger

""" This module provides common functionality used tools. """

logger = get_logger("Tool")


def interval_gen(base: int = 15, max: int = 300, step: int = 20):
    """Generator that yields an interval of time to wait between checks.
    The interval starts at the base value and increases by the step value"""
    current_value = base
    while True:
        yield current_value
        inc = step if current_value < max else 0
        current_value += inc


class WorkContext:
    """Provides data and functions for the tool to perform its assigned work."""

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


class ToolWrangler:
    """Manages the interaction between the tool and the rho-service to perform work.
    The actual work is performed by a function passed to the run method."""

    def __init__(self, tool_id: str):
        self.tool_id: str = tool_id
        self.work_context = WorkContext(self)

    def run(self, do_work: callable):
        """Run the tool with the provided function to perform the work."""
        self.logger = get_logger(self.tool_id)
        self.logger.info(f"Starting tool with id {self.tool_id}")
        while True:
            self.work_context.clear()
            self.ready_for_work()
            self.get_work()
            if not do_work(self.work_context):
                break

    def ready_for_work(self):
        """Designate the tool as ready to receive work."""
        interval = interval_gen()
        while True:
            outcome: apx.Outcome = apx.tool_update_ready(self.tool_id)
            self.logger.info(outcome)
            if outcome.success:
                return
            wait = next(interval)
            self.logger.info(
                f"Waiting {wait} seconds to check for tool to be unassigned"
            )
            sleep(wait)

    def get_work(self):
        """Get the work assignment for the tool."""
        interval = interval_gen()
        while True:
            work: apx.WorkInfo = apx.tool_details_work_assignment(self.tool_id)
            if not work.work_id:
                wait = next(interval)
                self.logger.info(f"Waiting {wait} seconds to check for assigned work")
                sleep(wait)
            else:
                self.work_context.set(work)
                return

    def send_report(self, work_id: str, report_create: apx.ReportCreate):
        """Send a report for the current work item."""
        apx.report_create(work_id, report_create)
        self.logger.info(
            f"Report sent for {work_id} with status {report_create.status}"
        )

    def send_successful(self, work_id: str):
        """Send a successful completion for the current work item."""
        apx.work_update_successful(work_id)
        self.logger.info(f"Successful completion sent for work item {work_id}")

    def send_failed(self, work_id: str):
        """Send a failed completion for the current work item."""
        apx.work_update_failed(work_id)
        self.logger.info(f"Failed completion sent for work item {work_id}")


def get_tool_id_from_env() -> str:
    """Get the tool id from the environment."""
    tool_id = os.environ.get("TOOL_ID")
    if not tool_id:
        print("TOOL_ID environment variable not set.")
        exit(1)
    logger.info(f"Starting tool with id {tool_id}")
    return tool_id


def run_as_tool(func):
    """Decorator to designate that the decorated function should be run as a tool.
    Creates an instance of ToolBase and passes it a reference to the function.
    """

    def wrapper(*args, **kwargs):
        if not kwargs.get("tool_id"):
            kwargs["tool_id"] = get_tool_id_from_env()
        ToolWrangler(kwargs["tool_id"]).run(func)

    return wrapper
