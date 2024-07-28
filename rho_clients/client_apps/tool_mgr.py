from threading import Thread
from time import sleep
from typing import List
from ..api import g_api as apx
from ..client_apps import tool_app as tap
from ..cmds import cmd_helpers as hp
from ..log_config import get_logger

rnd_int = hp.random_int_generator(0, 3)

logger = get_logger("ToolMgr")


class ToolMgr:
    """This class runs a given number of tools in separate threads"""

    def __init__(self, num_tools: int = 10) -> None:
        self.thread: Thread = None
        self.num_tools = num_tools
        self.tool_creates: List[apx.ToolCreate] = []
        self.tools_threads: List[Thread] = []

    def run(self):
        self.thread = self.run_tool_mgr_in_thread()

    def run_tool_mgr_in_thread(self) -> Thread:
        for _ in range(self.num_tools):
            tool_create = self.make_tool()
            sleep(next(rnd_int))
            thread = self.run_tool_in_thread(tool_create.tool_id)
            self.tools_threads.append(thread)

    def make_tool(self):
        tool_create = hp.make_tool_create()
        self.tool_creates.append(tool_create)
        apx.tool_create(tool_create)
        logger.info(f"Tool created: {tool_create.tool_id}")
        return tool_create

    def run_tool_in_thread(self, tool_id) -> Thread:
        thread = Thread(target=tap.simulate_work, kwargs={"tool_id": tool_id})
        thread.start()
        return thread


# create, enable, and delete tools
# monitor tool use stats
