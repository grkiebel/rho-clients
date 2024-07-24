from .assigner_app import MatchCheckerBase
from ..cmds import sim as sim


""" 
This module defines the application-specific data models
for the payloads managed by the rho-service.
"""


TASK_TYPE = "task_type"
MAX_PRIORITY = "max_priority"
PROCESSOR = "processor"
PRIORITY = "priority"
STAGE = "stage"
ACTION = "action"

tool_skills_template = {
    TASK_TYPE: sim.task_type,
    MAX_PRIORITY: sim.priority,
    PROCESSOR: sim.tool_processor,
}

task_needs_template = {
    TASK_TYPE: sim.task_type,
    PRIORITY: sim.priority,
    PROCESSOR: sim.task_processor,
}

report_details_template = {
    STAGE: sim.stage,
    ACTION: sim.action,
}


class AppMatchChecker(MatchCheckerBase):
    """Check if a tool can service a task- modify as needed"""

    def __init__(self):
        super().__init__()

        self.comparators = [
            lambda needs, skills: needs[TASK_TYPE] == skills[TASK_TYPE],
            lambda needs, skills: needs[PRIORITY] >= skills[MAX_PRIORITY],
            lambda needs, skills: needs[PROCESSOR] in ["", skills[PROCESSOR]],
        ]
        self.task_sort_key = lambda task: task.task_needs[PRIORITY]
        self.is_match = lambda task_needs, tool_skills: all(
            func(task_needs, tool_skills) for func in self.comparators
        )
