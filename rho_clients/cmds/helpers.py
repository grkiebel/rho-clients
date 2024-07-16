from typing import List
from ..api import g_api as apx
from ..cmds import y_sim as sim
from ..client_apps import y_app_models as yam


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


def verify_service_status():
    try:
        response = apx.read_root()
        print(response)
        return True
    except Exception as e:
        print(e)
        return False


def make_task_create_list(num_tasks: int = 5) -> List[apx.TaskCreate]:
    result = []
    for _ in range(num_tasks):
        task_needs = sim.populate(yam.task_needs_template)
        task_id = sim.task_id()
        task_create_rep = apx.TaskCreate(task_id=task_id, task_needs=task_needs)
        result.append(task_create_rep)
    return result


def make_tool_create_list(num_tools: int = 5) -> List[apx.ToolCreate]:
    result = []
    for _ in range(num_tools):
        tool_skills = sim.populate(yam.tool_skills_template)
        tool_id = sim.tool_id()
        tool_create_rep = apx.ToolCreate(tool_id=tool_id, tool_skills=tool_skills)
        result.append(tool_create_rep)
    return result


def make_report_create_list(num_reports: int = 5) -> List[apx.ReportCreate]:
    result = []
    for _ in range(num_reports):
        report_details = sim.populate(yam.report_details_template)
        report_create = apx.ReportCreate(status=sim.state(), details=report_details)
        result.append(report_create)
    return result
