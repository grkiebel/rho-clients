from typing import List, Set, Tuple
from ..api import g_api as apx
from ..log_config import get_logger

logger = get_logger("Assigner")

assignment_matchers = {"default": lambda tools, tasks: (tools, tasks)}
assignment_sorters = {"default": lambda task, tool: True}


def assignment_sorter(key: str):
    """Decorator to register a function as a sorter for the given key"""

    def decorator(func):
        assignment_sorters[key] = func
        return func

    return decorator


def assignment_matcher(key: str):
    """Decorator to register a function as a matcher for the given key"""

    def decorator(func):
        assignment_matchers[key] = func
        return func

    return decorator


def find_assignments(key: str = "default") -> List[Tuple[str, str]]:
    sorter = assignment_sorters.get(key)
    matcher = assignment_matchers.get(key)
    if not sorter or not matcher:
        logger.error(f"Sorter and/or matcher not found for key: {key}")
        return []

    logger.info(f"Using key '{key}' for sorter and matcher")

    tools, tasks = sorter(apx.tool_list_available(), apx.task_list_available())
    if not tools or not tasks:
        logger.info("No work candidates availble")
        return []

    pairs: List[(str, str)] = []  # List of matched pairs as (tool_id, task_id) tuples
    used_tools: Set[apx.BasicTool] = set()
    used_tasks: Set[apx.BasicTask] = set()
    for tool in tools:
        for task in tasks:
            if matcher(task, tool):
                tool_id = tool.tool_id
                task_id = task.task_id
                if task_id not in used_tasks and tool_id not in used_tools:
                    used_tasks.add(task_id)
                    used_tools.add(tool_id)
                    pairs.append((tool_id, task_id))
    logger.info(f"Found {len(pairs)} assignment(s)")
    return pairs
