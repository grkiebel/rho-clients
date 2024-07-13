from typing import List, Set
from ..access import g_api as apx
from ..log_config import get_logger

logger = get_logger("Assigner")


class MatchCheckerBase:
    """
    Base class for for class that determines if a tool can service a task.
    """

    def __init__(self):
        self.task_sort_key = None  # default: no task sorting
        self.is_match = lambda task, tool: True  # default: always match


class WorkFinder:

    def __init__(
        self,
        match_checker: MatchCheckerBase,
    ):
        self.matches: List[(apx.BasicTool, apx.BasicTask)] = []
        self.pairs: List[(str, str)] = []
        self.sort_key = match_checker.task_sort_key
        self.is_match = match_checker.is_match

        # get all available tools and tasks
        self.tools: List[apx.BasicTool] = apx.tool_list_available()
        self.tasks: List[apx.BasicTask] = apx.task_list_available()
        if not self.tools or not self.tasks:
            logger.info("No work candidates availble")
            return
        logger.info(f"Found {len(self.tools)} tool(s) and {len(self.tasks)} task(s)")

        # get all possible matches between tools and tasks
        if self.sort_key:
            self.tasks.sort(key=self.sort_key)
        self.matches = [
            (tool, task)
            for tool in self.tools
            for task in self.tasks
            if self.is_match(task, tool)
        ]
        logger.info(f"Found {len(self.matches)} potential matche(s)")

        # Remove duplicate task and tool assignments."""
        used_tools: Set[apx.BasicTool] = set()
        used_tasks: Set[apx.BasicTask] = set()
        for tool, task in self.matches:
            tool_id = tool.tool_id
            task_id = task.task_id
            if task_id not in used_tasks and tool_id not in used_tools:
                used_tasks.add(task_id)
                used_tools.add(tool_id)
                self.pairs.append((tool_id, task_id))
        logger.info(f"Filtered down to {len(self.pairs)} assignment(s)")
