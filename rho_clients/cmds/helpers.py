import random
from typing import List
from ..api import g_api as apx
from . import sim
from ..client_apps import app_models as cam
from ..client_apps.assigner_app import find_assignments
import os


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
        report_details = sim.populate(cam.report_details_template)
        report_create = apx.ReportCreate(status=sim.state(), details=report_details)
        result.append(report_create)
    return result


def make_work_create_list(num_work_items: int = 1) -> List[apx.WorkCreate]:
    pairs = find_assignments(cam.AppMatchChecker())
    pairs = pairs[:num_work_items]
    result = []
    for tool_id, task_id in pairs:
        work_create = apx.WorkCreate(tool_id=tool_id, task_id=task_id)
        result.append(work_create)
    return result


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


def make_task_create():
    task_needs = sim.populate(cam.task_needs_template)
    task_id = sim.task_id()
    task_create = apx.TaskCreate(task_id=task_id, task_needs=task_needs)
    return task_create


def make_tool_create():
    tool_skills = sim.populate(cam.tool_skills_template)
    tool_id = sim.tool_id()
    tool_create = apx.ToolCreate(tool_id=tool_id, tool_skills=tool_skills)
    return tool_create


def random_int_generator(min_value: int, max_value: int):
    random.seed(os.getpid())
    while True:
        yield random.randint(min_value, max_value)


def verify_service_status():
    try:
        response = apx.general_status()
        print(response)
        return True
    except Exception as e:
        print(e)
        return False
