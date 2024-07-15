import random
from typing import List
from ..api import g_api as apx
from ..client_apps import app_models as apm, assigner_app as asn
from .sim_words import generate_random_sentence, generate_random_state


class Sim:
    def __init__(self): ...

    def priority(self):
        return random.randint(1, 3)

    def task_type(self):
        return random.choice(["Red", "Green", "Blue"])

    def processor(self, name):
        name = name.lower()
        if "tool" in name:
            return random.choice(["alpha", "beta", "gamma"])
        if "task" in name:
            return random.choice(["", "", "", "", "", "alpha", "beta", "gamma"])

    def task_id(self):
        letter = chr(random.randint(65, 90))
        n1 = random.randint(10, 99)
        n2 = random.randint(1000, 9999)
        return f"Task-{n1}-{letter}-{n2}"

    def tool_id(self):
        letter1 = chr(random.randint(65, 90))
        letter2 = chr(random.randint(65, 90))
        n1 = random.randint(10, 99)
        n2 = random.randint(1000, 9999)
        return f"Tool-{letter1}{letter2}-{n2}"

    def instance(self, klass):
        instance = klass()  # Create an instance of the class
        name = klass.__name__  # Get the name of the class
        instance_attributes = vars(instance)  # Get the attributes of the instance
        for attribute in instance_attributes:
            # Set the applicable attributes of the instance
            if attribute == "task_type":
                setattr(instance, attribute, self.task_type())
            if attribute == "max_priority":
                setattr(instance, attribute, self.priority())
            if attribute == "processor":
                setattr(instance, attribute, self.processor(name))
            if attribute == "priority":
                setattr(instance, attribute, self.priority())
            if attribute == "stage":
                setattr(instance, attribute, generate_random_state())
            if attribute == "action":
                setattr(instance, attribute, generate_random_sentence())

        return instance

    def make_task_create_list(self, num_tasks: int = 5) -> List[apx.TaskCreate]:
        result = []
        for _ in range(num_tasks):
            task_needs = self.instance(apm.TaskNeeds).model_dump()
            task_id = self.task_id()
            task_create = apx.TaskCreate(task_id=task_id, task_needs=task_needs)
            result.append(task_create)
        return result

    def make_tool_create_list(self, num_tools: int = 5) -> List[apx.ToolCreate]:
        result = []
        for _ in range(num_tools):
            tool_skills = self.instance(apm.ToolSkills).model_dump()
            tool_id = self.tool_id()
            tool_create = apx.ToolCreate(tool_id=tool_id, tool_skills=tool_skills)
            result.append(tool_create)
        return result

    def make_report_create_list(self, num_reports: int = 3) -> List[apx.ReportCreate]:
        result = []
        for _ in range(num_reports):
            report_details = self.instance(apm.ReportDetails).model_dump()
            report_create = apx.ReportCreate(
                status=generate_random_state(), details=report_details
            )
            result.append(report_create)
        return result
