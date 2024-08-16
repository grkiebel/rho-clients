from threading import Thread
from time import sleep
from typing import List
from ..api import g_api as apx
from ..client_apps import tool_app as tap
from ..cmds import cmd_helpers as hp
from ..log_config import get_logger

rnd_int = hp.random_int_generator(0, 3)

logger = get_logger("ToolMgr")

""" This module simulates the creation and use of tools. 
In a real-world scenario, tools would be managed some sort of 
system dashboard or admin interface. 
"""

tool_pids = {}

# get list of tools from rho-service
# if tool is already managed and running, do nothing
# if tool is already managed and not running, start it
# if tool is not managed, launch it (subprocess or thread)
# if tool is managed, but not in rho-service, stop it and unmanage it
