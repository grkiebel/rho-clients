from ..generated import g_api as apx
from ..log_config import get_logger
from ..cmds.sim import Sim

sim = Sim()

apx.initialize("http://localhost:8080", get_logger("API-Access"))


def verify_service_status():
    try:
        response = apx.read_root()
        print(response)
        return True
    except Exception as e:
        print(e)
        return False


def display_result(obj):
    obj_type = type(obj)
    if obj_type == list:
        for item in obj:
            print(vars(item))
    elif obj_type == dict:
        print(obj)
    elif obj_type == apx.Outcome:
        print(obj)
    else:
        for attr, value in vars(obj).items():
            print(f"{attr}: {value}")


# ------------------- general ops -------------------


# def clear_all():
#     tool_clear()
#     task_clear()
#     report_clear()
#     work_clear()
#     archive_clear()


# def service_status():
#     result = apx.read_root()
#     display_result(result)
