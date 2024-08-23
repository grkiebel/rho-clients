import argparse
from . import cmd_helpers as hp
from ..log_config import get_logger
from ..generated import g_api as apx
from ..client_apps.x_tool_mgr import ToolMgr
from ..client_apps.task_mgr import TaskMgr
from ..client_apps.assigner_mgr import AssignerMgr
from ..client_apps.work_mgr import WorkMgr

""" This module runs a full scale simulated operation 
of the various rho-service clients. """


def start(num_tools: int = 10, num_tasks: int = 20):
    hp.clear_db()

    tool_mgr = ToolMgr(num_tools)
    task_mgr = TaskMgr(num_tasks)
    assigner_mgr = AssignerMgr()
    work_mgr = WorkMgr()

    tool_mgr.run()
    task_mgr.run()
    assigner_mgr.run()
    work_mgr.run()


def main():
    args = get_args()
    apx.initialize(args.rho_service_url, get_logger("API-Access"))
    start(num_tasks=args.num_tasks, num_tools=args.num_tools)


def get_args():
    parser = argparse.ArgumentParser(description="API Generator")
    parser.add_argument(
        "-url",
        "--rho_service_url",
        help="URL to the rho-service",
        default="http://localhost:8080",
    )
    parser.add_argument(
        "-tls",
        "--num_tools",
        help="Number of tools to create",
        default=10,
    )
    parser.add_argument(
        "-tks",
        "--num_tasks",
        help="Number of tasks to create",
        default=20,
    )
    args = parser.parse_args()
    return args
