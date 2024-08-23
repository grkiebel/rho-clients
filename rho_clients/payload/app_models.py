from enum import Enum
from typing import List, Tuple
from ..generated import g_api as apx
from ..client_apps import assigner_app as asn


""" 
This module defines the application-specific data models
for the payloads managed by the rho-service.  This is an
example for a simple tool sills and task needs model.
Modify or replace as needed for your actual application.
"""


class SkKeys(Enum):
    TASK_TYPE = "task_type"
    MAX_PRIORITY = "max_priority"
    PROCESSOR = "processor"


class NdKeys(Enum):
    TASK_TYPE = "task_type"
    PRIORITY = "priority"
    PROCESSOR = "processor"


class RpKeys(Enum):
    STAGE = "stage"
    ACTION = "action"


tool_skills_template = {
    SkKeys.TASK_TYPE.value: "",
    SkKeys.MAX_PRIORITY.value: 0,
    SkKeys.PROCESSOR.value: "",
}


task_needs_template = {
    NdKeys.TASK_TYPE.value: "",
    NdKeys.PRIORITY.value: 0,
    NdKeys.PROCESSOR.value: "",
}


report_details_template = {
    RpKeys.STAGE.value: "",
    RpKeys.ACTION.value: "",
}


# register this function with the assigner as a sorter under the key "primary"
@asn.assignment_sorter("primary")
def sorter(tools: List[apx.BasicTool], tasks: List[apx.BasicTask]) -> Tuple[List, List]:
    """sort the tools and tasks"""
    tools.sort(key=lambda tool: tool.ready_since)
    tasks.sort(
        key=lambda task: (task.task_needs[NdKeys.PRIORITY.value], task.created_at)
    )
    return tools, tasks


# register this function with the assigner as a matcher under the key "primary"
@asn.assignment_matcher("primary")
def matcher(task: apx.BasicTask, tool: apx.BasicTool) -> bool:
    """determine if a task and tool are a match"""
    needs = task.task_needs
    skills = tool.tool_skills
    hits: List[bool] = []
    hits.append(needs[NdKeys.TASK_TYPE.value] == skills[SkKeys.TASK_TYPE.value])
    hits.append(needs[NdKeys.PRIORITY.value] >= skills[SkKeys.MAX_PRIORITY.value])
    hits.append(needs[NdKeys.PROCESSOR.value] in ["", skills[SkKeys.PROCESSOR.value]])
    return all(hits)
