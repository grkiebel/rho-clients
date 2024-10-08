import random
from time import sleep
from typing import List
from ..client_apps.tool_base import WorkContext, run_as_tool
from ..cmd_shell import cmd_helpers as hp
from ..generated import g_api as apx

""" This code simulates a tool that performs work and sends reports and a completion. """

keep_running = False  # Set to True to keep the tool running


@run_as_tool
def simulate_work(context: WorkContext) -> bool:
    context.logger.info(f"Simulating work for {context.work_id}")

    num_reports = random.randint(1, 4)
    report_list: List[apx.report_create] = hp.make_report_create_list(num_reports)
    for report_create in report_list:
        context.send_report(context.work_id, report_create)
        sleep(random.randint(1, 3))

    context.send_successful(context.work_id)
    return keep_running


def main():
    simulate_work(tool_id="12345")


if __name__ == "__main__":
    main()
