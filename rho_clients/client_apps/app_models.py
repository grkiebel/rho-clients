from pydantic import BaseModel
from .assigner_app import MatchCheckerBase


""" 
This module defines the application-specific data models and 
application-specific match checker class that determines if a tool can service a task.
"""


class ToolSkills(BaseModel):
    """ " This class is required, but its attributes can be modified as needed"""

    task_type: str = ""
    max_priority: int = 0
    processor: str = ""
    # TODO: description: str = ""


class TaskNeeds(BaseModel):
    """ " This class is required, but its attributes can be modified as needed"""

    task_type: str = ""
    priority: int = 0
    processor: str = ""
    # TODO: description: str = ""
    # TODO: settings: dict = {}
    # TODO: resource_locations: dict = {}


class ReportDetails(BaseModel):
    """ " This class is required, but its attributes can be modified as needed"""

    stage: str = ""
    action: str = ""
    # TODO: note: str = ""


class AppMatchChecker(MatchCheckerBase):
    """Check if a tool can service a task- modify as needed"""

    def __init__(self):
        self.comparators = [
            lambda needs, skills: needs["task_type"] == skills["task_type"],
            lambda needs, skills: needs["priority"] >= skills["max_priority"],
            lambda needs, skills: needs["processor"] in ["", skills["processor"]],
        ]
        self.task_sort_key = lambda task: task.task_needs["priority"]
        self.is_match = lambda task, tool: all(
            func(task.task_needs, tool.tool_skills) for func in self.comparators
        )


class Context:
    tool_skills_class = ToolSkills
    task_needs_class = TaskNeeds
    report_details_class = ReportDetails
    match_checker_class = AppMatchChecker
