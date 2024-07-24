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
    report_details_list: List[dict] = hp.make_report_details(num_reports)
    for report_details in report_details_list:
        context.send_report(context.work_id, "Processing", report_details)
        sleep(random.randint(1, 3))

    context.send_successful(context.work_id)
    return True  # Return True to indicate work was successful


def main():
    simulate_work(work_id="12345")


if __name__ == "__main__":
    main()
