from ast import main
from typing import List
from ..cmd_shell import cmd_helpers as hp
from ..log_config import get_logger
from ..generated import g_api as apx
import subprocess

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
# if tool is managed, but not in rho-service, kill it and unmanage it

# ...

# # Create a subprocess
# subprocess_obj = subprocess.Popen(["command", "arg1", "arg2"])

# # Store the subprocess PID in the tool_pids dictionary
# tool_pids[subprocess_obj.pid] = subprocess_obj

# # ...
# # Check the status of the subprocess
# status = subprocess_obj.poll()

# if status is None:
#     print("Subprocess is still running")
# else:
#     print(f"Subprocess has completed with exit status: {status}")

# # Terminate a subprocess
# subprocess_obj.terminate()
# del tool_pids[subprocess_obj.pid]


# maintain data about tools that are already being managed
# - sqlite? json? csv? in-memory?

# modify tool_app.py to get its tool_id from the command line (or environment variable? or either?)

# ----------------------------------------------------


def update_tools():
    tools: List[apx.BriefTool] = apx.tool_list()


def main(service_url: str = None):
    # if not service_url:
    #     service_url = get_args()
    apx.initialize(service_url, get_logger("API-Access"))
    update_tools()


if __name__ == "__main__":
    main(service_url="http://localhost:8080")
