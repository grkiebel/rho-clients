from typing import List, Set, Tuple
from ..api import g_api as apx
from ..log_config import get_logger

logger = get_logger("Assigner")


class MatchCheckerBase:
    """
    Base class for for class that determines if a tool can service a task.
    """

    def __init__(self):
        self.task_sort_key = None  # default: no task sorting
        self.tool_sort_key = None  # default: no tool sorting
        self.is_match = lambda task_needs, tool_skills: True  # default: always match


def find_assignments(match_checker: MatchCheckerBase) -> List[Tuple[str, str]]:
    pairs: List[(str, str)] = []  # List of matched pairs as (tool_id, task_id) tuples
    task_sort_key = match_checker.task_sort_key
    tool_sort_key = match_checker.tool_sort_key
    is_match = match_checker.is_match

    tools: List[apx.BasicTool] = apx.tool_list_available()
    tasks: List[apx.BasicTask] = apx.task_list_available()
    if not tools or not tasks:
        logger.info("No work candidates availble")
        return []

    if task_sort_key:
        tasks.sort(key=task_sort_key)
    if tool_sort_key:
        tools.sort(key=tool_sort_key)

    used_tools: Set[apx.BasicTool] = set()
    used_tasks: Set[apx.BasicTask] = set()
    for tool in tools:
        for task in tasks:
            if is_match(task.task_needs, tool.tool_skills):
                tool_id = tool.tool_id
                task_id = task.task_id
                if task_id not in used_tasks and tool_id not in used_tools:
                    used_tasks.add(task_id)
                    used_tools.add(tool_id)
                    pairs.append((tool_id, task_id))
    logger.info(f"Found {len(pairs)} assignment(s)")

    return pairs
