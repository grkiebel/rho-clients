import random
from time import sleep
from typing import List
from .tool_base import WorkContext, run_as_tool
from ..cmds import helpers as hp
from ..api import g_api as apx


@run_as_tool
def simulate_work(context: WorkContext) -> bool:
    context.logger.info(f"Simulating work for {context.work_id}")

    num_reports = random.randint(1, 4)
    report_list: List[apx.report_create] = hp.make_report_create_list(num_reports)
    for report_create in report_list:
        context.send_report(context.work_id, report_create)
        sleep(random.randint(1, 3))

    context.send_successful(context.work_id)
    return True  # Return True to indicate work was successful


def main():
    simulate_work(tool_id="12345")


if __name__ == "__main__":
    main()
