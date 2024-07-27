from typing import List, Tuple
from ..cmds import sim as sim
from ..api import g_api as apx
from ..client_apps import assigner_app as asn


""" 
This module defines the application-specific data models
for the payloads managed by the rho-service.  This is an
example for a simple tool sills and task needs model.
Modify or replace as needed for your actual application.
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


@asn.assignment_sorter("primary")
def sorter(tools: List[apx.BasicTool], tasks: List[apx.BasicTask]) -> Tuple[List, List]:
    """sort the tools and tasks"""
    tools.sort(key=lambda tool: tool.ready_since)
    tasks.sort(key=lambda task: (task.task_needs[PRIORITY], task.created_at))
    return tools, tasks


@asn.assignment_matcher("primary")
def matcher(task: apx.BasicTask, tool: apx.BasicTool) -> bool:
    """determine if a task and tool are a match"""
    needs = task.task_needs
    skills = tool.tool_skills
    hits: List[bool] = []
    hits.append(needs[TASK_TYPE] == skills[TASK_TYPE])
    hits.append(needs[PRIORITY] >= skills[MAX_PRIORITY])
    hits.append(needs[PROCESSOR] in ["", skills[PROCESSOR]])
    return all(hits)
