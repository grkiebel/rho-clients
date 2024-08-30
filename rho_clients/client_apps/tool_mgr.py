from typing import Callable
from time import sleep
from ..generated import g_api as apx
from ..log_config import get_logger

logger = get_logger("ToolMgr")

""" 
This module manages assigning processors to do work. 
"""

# ----------------------------------------------------
"""
work manager

- add processor_type to tools table (also add to ToolCreate model)

- add processor_id to work table (null when work created)

- tool_processor_manager:
  - for each work item
    - if work is completed, 
      - check if processor is still running and issue a warning if it is
      - continue
    - if processor_id is null, 
      - spin up appropriate processor
      - update processor_id
    - if processor_id is not null
      - check if processor is still running and issue a warning if not

- when work is completed, set processor_id to null

"""

"""
run work manager in container and consider celery


"""


processor_lookup: Callable = None


def tool_processor_lookup() -> Callable:
    """Decorator to register a function as a processor lookup function"""

    def decorator(func):
        global processor_lookup
        processor_lookup = func
        return func

    return decorator


class ToolProcessManager:
    def __init__(self):
        pass

    def update(self):
        pass


def manage_tools(interval: int = 5) -> None:
    tool_process_mgr = ToolProcessManager()
    while True:
        tool_process_mgr.update()
        sleep(interval)


# ----------------------------------------------------


def main(service_url: str = None) -> None:
    # TODO: get service_url and other parameters from command line or environment variables
    apx.initialize(service_url, get_logger("API-Access"))
    manage_tools()


if __name__ == "__main__":
    main(service_url="http://localhost:8080")
