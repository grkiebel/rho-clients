import random
from time import sleep
from generated import ToolBase, WorkContext, get_tool_id
from ..cmds.sim import SimReportDetails


class ToolWorker:
    def __init__(self, tool_id: str):
        self.tool_id = tool_id

    def run(self):
        ToolBase(self.tool_id).run(self.do_work)

    def do_work(self, context: WorkContext) -> bool:
        context.logger.info(f"Simulating work for {context.work_id}")
        for i in range(1, random.randint(1, 4)):
            details = SimReportDetails.details_dict()
            context.send_report(context.work_id, "Processing", details)
            sleep(random.randint(3, 7))
        details = SimReportDetails.details_dict()
        context.send_successful(context.work_id, details)
        return True  # Return True to indicate work was successful


def main():
    tool_id = get_tool_id()
    tool_worker = ToolWorker(tool_id)


if __name__ == "__main__":
    main()
