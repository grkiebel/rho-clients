import os
import random
from typing import List
from ..app_specific.sim_creates import (
    make_tool_create,
    make_task_create,
    make_report_create,
)
from ..generated import g_api as apx
from ..client_apps import assigner_app as asn

""" This module provides functionality needed by the cmds generated 
from the rho-service api_schema. """


def random_int_generator(min_value: int, max_value: int):
    """Generator that yields a random integer between the min and max values"""
    random.seed(os.getpid())
    while True:
        yield random.randint(min_value, max_value)


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


def display_result(obj, label: str = ""):
    print(f"\n==== {label} ====")
    if obj is None:
        print("None")
        return
    obj_type = type(obj)
    if obj_type == list:
        for item in obj:
            print(vars(item))
        print(f"Total: {len(obj)}")
    elif obj_type == dict:
        print(obj)
    elif obj_type == apx.Outcome:
        print(obj)
    else:
        for attr, value in vars(obj).items():
            print(f"{attr}: {value}")


def make_tool_create_list(num_tools: int = 5) -> List[apx.ToolCreate]:
    result = []
    for _ in range(num_tools):
        tool_create = make_tool_create()
        result.append(tool_create)
    return result


def make_task_create_list(num_tasks: int = 5) -> List[apx.TaskCreate]:
    result = []
    for _ in range(num_tasks):
        task_create = make_task_create()
        result.append(task_create)
    return result


def make_report_create_list(num_reports: int = 5) -> List[apx.ReportCreate]:
    result = []
    for _ in range(num_reports):
        report_create = make_report_create()
        result.append(report_create)
    return result


def make_work_create_list(num_work_items: int = 1) -> List[apx.WorkCreate]:
    pairs = asn.find_assignments(s_key="primary", m_key="primary")
    pairs = pairs[:num_work_items]
    result = []
    for tool_id, task_id in pairs:
        work_create = apx.WorkCreate(tool_id=tool_id, task_id=task_id)
        result.append(work_create)
    return result
