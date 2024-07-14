from ..api import g_api as apx


def display_ops_result(obj):
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
