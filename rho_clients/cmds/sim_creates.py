import random
from .sim_words import sentence, state
from ..api import g_api as apx
from ..client_apps import app_models as cam

""" Generate simulated data for testing and command shell commands """


def make_tool_create():
    tool_skills = populate(cam.tool_skills_template, tool_skills_sim_fields)
    tool_id = _tool_id()
    tool_create = apx.ToolCreate(tool_id=tool_id, tool_skills=tool_skills)
    return tool_create


def make_task_create():
    task_needs = populate(cam.task_needs_template, task_needs_sim_fields)
    task_id = _task_id()
    task_create = apx.TaskCreate(task_id=task_id, task_needs=task_needs)
    return task_create


def make_report_create():
    report_details = populate(cam.report_details_template, report_details_sim_fields)
    report_create = apx.ReportCreate(status=state(), details=report_details)
    return report_create


def populate(template: dict, sim_fields: dict) -> dict:
    fields = {key: sim_func() for key, sim_func in sim_fields.items()}
    bob = {key: fields[key] for key in template.keys() if key in fields.keys()}
    return bob


def priority():
    return random.randint(1, 3)


def task_type():
    return random.choice(["Red", "Green", "Blue"])


def tool_processor():
    return random.choice(["alpha", "beta", "gamma"])


def task_processor():
    return random.choice(["", "", "", "", "", "alpha", "beta", "gamma"])


def stage():
    return state()


def action():
    return sentence()


def _task_id():
    letter = chr(random.randint(65, 90))
    n1 = random.randint(10, 99)
    n2 = random.randint(1000, 9999)
    return f"Task-{n1}-{letter}-{n2}"


def _tool_id():
    letter1 = chr(random.randint(65, 90))
    letter2 = chr(random.randint(65, 90))
    n1 = random.randint(10, 99)
    n2 = random.randint(1000, 9999)
    return f"Tool-{letter1}{letter2}-{n2}"


tool_skills_sim_fields = {
    cam.SkKeys.TASK_TYPE.value: task_type,
    cam.SkKeys.MAX_PRIORITY.value: priority,
    cam.SkKeys.PROCESSOR.value: tool_processor,
}


task_needs_sim_fields = {
    cam.NdKeys.TASK_TYPE.value: task_type,
    cam.NdKeys.PRIORITY.value: priority,
    cam.NdKeys.PROCESSOR.value: task_processor,
}


report_details_sim_fields = {
    cam.RpKeys.STAGE.value: stage,
    cam.RpKeys.ACTION.value: action,
}
