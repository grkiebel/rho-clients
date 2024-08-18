from typing import List, Set, Tuple
from ..generated import g_api as apx
from ..log_config import get_logger

""" This module provides a set of tool/tasks assignments based 
on the registered sorters and matchers. """

logger = get_logger("Assigner")

assignment_matchers = {"null": lambda tools, tasks: (tools, tasks)}
assignment_sorters = {"null": lambda task, tool: True}


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


def find_assignments(s_key: str = "null", m_key: str = "null") -> List[Tuple[str, str]]:
    """Find assignments using the sorter and matcher registered under the given keys"""
    sorter = assignment_sorters.get(s_key)
    matcher = assignment_matchers.get(m_key)
    if not sorter or not matcher:
        logger.error(f"Sorter and/or matcher not found for keys: {s_key}, {m_key}")
        return []

    logger.info(f"Using sorter key '{s_key}' and matcher key '{m_key}'")

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
