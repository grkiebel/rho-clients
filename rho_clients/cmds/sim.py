import random
from .sim_words import sentence, state


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


def task_id():
    letter = chr(random.randint(65, 90))
    n1 = random.randint(10, 99)
    n2 = random.randint(1000, 9999)
    return f"Task-{n1}-{letter}-{n2}"


def tool_id():
    letter1 = chr(random.randint(65, 90))
    letter2 = chr(random.randint(65, 90))
    n1 = random.randint(10, 99)
    n2 = random.randint(1000, 9999)
    return f"Tool-{letter1}{letter2}-{n2}"


def populate(template: dict):
    return {key: sim_func() for key, sim_func in template.items()}
