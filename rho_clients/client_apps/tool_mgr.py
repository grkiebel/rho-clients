from datetime import datetime
from typing import List
from time import sleep
from sqlmodel import Field, SQLModel, create_engine, Session, select
from ..generated import g_api as apx
from ..log_config import get_logger

logger = get_logger("ToolMgr")

""" 
This module simulates the creation and use of tools. 
"""


# ----------------------------------------------------
"""
Tool manager can either be the source of tools or demand driven from work
"""

"""
app_specific.app_tool_config -> maps tool skills to process command

"""

"""
As tool source:
- tools are created and deleted by the tool manager
- tool manager (and tool processors) will add/delete/update tools in the service
"""

"""
As demand driven:
- tools are created and deleted in the service
- tool manager will create/delete/update tool processors 
  according to tool/work status in the service



"""


# ----------------------------------------------------


class ToolProcessor(SQLModel, table=True):
    __tablename__ = "managed_tools"
    tool_id: str = Field(primary_key=True)
    enabled: bool = Field(default=None)
    ready_since: datetime | None = Field(default=None)
    command: str = Field(default="tool_app.py")
    process_id: str | None = Field(default=None)

    @classmethod
    def from_tool(cls, tool: apx.BriefTool) -> "ToolProcessor":
        return cls(
            tool_id=tool.tool_id,
            enabled=tool.enabled,
            ready_since=tool.ready_since,
            orphaned=False,
        )


def manage_tool_process(managed_tool: ToolProcessor) -> None:
    pass


class ToolProcessManager:
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///tools.db")
        SQLModel.metadata.create_all(self.engine)

    def update(self, service_tools: List[apx.BriefTool]) -> None:
        self._synch_managed_tools(service_tools)
        self._manage_processes()

    def bob(self):
        tools_in_service = apx.tool_list()
        working_tools = [tool for tool in tools_in_service if tool.work_id]

    # def _manage_processes(self) -> None:
    #     with Session(self.engine) as session:
    #         managed_tools = session.exec(select(ToolProcessor)).all()
    #         for tool in managed_tools:
    #             manage_tool_process(tool)

    # def _synch_managed_tools(self, service_tools: List[apx.BriefTool]) -> None:
    #     with Session(self.engine) as session:
    #         managed_tools = session.exec(select(ToolProcessor)).all()
    #         managed_tools_ids = [t.tool_id for t in managed_tools]
    #         service_tools_ids = [t.tool_id for t in service_tools]
    #         self._add_unmanaged_tools(session, service_tools, managed_tools_ids)
    #         self.delete_unused_tools(session, managed_tools, service_tools_ids)
    #         session.commit()

    # def _add_unmanaged_tools(self, session, service_tools, managed_tools_ids):
    #     for tool in service_tools:
    #         if tool.tool_id not in managed_tools_ids:
    #             managed_tool = ToolProcessor.from_tool(tool)
    #             session.add(managed_tool)

    # def delete_unused_tools(self, session, managed_tools, service_tools_ids):
    #     for managed_tool in managed_tools:
    #         if managed_tool.tool_id not in service_tools_ids:
    #             session.delete(managed_tool)


def manage_tools(interval: int = 5) -> None:
    tool_process_mgr = ToolProcessManager()
    while True:
        tools: List[apx.BriefTool] = apx.tool_list()
        tool_process_mgr.update(tools)
        sleep(interval)


def main(service_url: str = None) -> None:
    # TODO: get service_url and other parameters from command line or environment variables
    apx.initialize(service_url, get_logger("API-Access"))
    manage_tools()


if __name__ == "__main__":
    main(service_url="http://localhost:8080")
