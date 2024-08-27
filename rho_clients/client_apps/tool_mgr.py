from calendar import c
from datetime import datetime
from multiprocessing import process
from typing import List
import subprocess
from time import sleep
from sqlmodel import Field, SQLModel, create_engine, Session
from threading import Thread
from ..cmd_shell import cmd_helpers as hp
from ..generated import g_api as apx
from ..log_config import get_logger

logger = get_logger("ToolMgr")

""" 
This module simulates the creation and use of tools. 
"""


# ----------------------------------------------------


# ----------------------------------------------------


class ManagedTool(SQLModel, table=True):
    __tablename__ = "managed_tools"
    tool_id: str = Field(primary_key=True)
    enabled: bool = Field(default=None)
    ready_since: datetime | None = Field(default=None)
    orphaned: bool = Field(default=False)
    command: str = Field(default="tool_app.py")
    process_id: str = Field(default=None)

    @classmethod
    def from_tool(cls, tool: apx.BriefTool) -> "ManagedTool":
        return cls(
            tool_id=tool.tool_id,
            enabled=tool.enabled,
            ready_since=None,
            orphaned=False,
        )


class ToolManager:
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///tools.db")
        SQLModel.metadata.create_all(self.engine)

    def update(self, current_tools: List[apx.BriefTool]) -> None:
        self._add_new_tools(current_tools)
        self._delete_old_tools(current_tools)

    def find(self, tool_id: str) -> ManagedTool:
        """Find a tool in tools list by its tool_id, return None if not found"""
        with Session(self.engine) as session:
            return (
                session.exec(ManagedTool).where(ManagedTool.tool_id == tool_id).first()
            )

    def _add_new_tools(self, current_tools: List[apx.BriefTool]):
        with Session(self.engine) as session:
            for current_tool in current_tools:
                if not self.find(current_tool.tool_id):
                    managed_tool = ManagedTool.from_tool(current_tool)
                    session.add(managed_tool)
            session.commit()

    def _delete_old_tools(self, current_tools) -> None:
        current_tools_ids = [t.tool_id for t in current_tools]
        with Session(self.engine) as session:
            managed_tools = session.exec(ManagedTool).all()
            for managed_tool in managed_tools:
                if managed_tool.tool_id not in current_tools_ids:
                    session.delete(managed_tool)
            session.commit()


def manage_tools(interval: int = 5) -> None:
    managed_tools = ToolManager()
    while True:
        tools: List[apx.BriefTool] = apx.tool_list()
        managed_tools.update(tools)
        sleep(interval)


def main(service_url: str = None) -> None:
    # TODO: get service_url and other parameters from command line or environment variables
    apx.initialize(service_url, get_logger("API-Access"))
    manage_tools()


if __name__ == "__main__":
    main(service_url="http://localhost:8080")


# # ----------------------------------------------------------------
# class DbURL:
#     """
#     This class constructs the database URL for the database file.
#     """

#     FOLDER_NAME = "databases"
#     FOLDER_PATH = os.path.join(os.getcwd(), FOLDER_NAME)
#     FILE_NAME = "msg_cache.db"

#     @classmethod
#     def get(cls, file_name: str = None) -> str:
#         """
#         Get path to log file, creating enclosing directory if necessary.
#         """
#         try:
#             # create folder if it doesn't exist
#             if not os.path.exists(cls.FOLDER_PATH):
#                 os.makedirs(cls.FOLDER_PATH)
#             # create database URL
#             file_name = file_name or cls.FILE_NAME
#             db_file_path = os.path.join(cls.FOLDER_PATH, file_name)
#             return f"sqlite:///{db_file_path}"
#         except Exception as e:
#             print(f"Error creating database URL: {str(e)}")
#             return None

# ----------------------------------------------------
# class ManagedToolBase:
#     def __init__(self, tool: apx.BriefTool):
#         self.tool_id = tool.tool_id
#         self.enabled = tool.enabled
#         self.orphaned = False
#         self.command = "tool_app.py"  # command line parameters or tool class name?

#     def start(self) -> None:
#         raise NotImplementedError

#     def stop(self) -> None:
#         raise NotImplementedError

#     def is_running(self) -> bool:
#         raise NotImplementedError


# class ManagedToolThread(ManagedToolBase):
#     def __init__(self, tool: apx.BriefTool):
#         super().__init__(tool)
#         self.thread_obj = None
#         self.process_command = "tool_app.py"

#     def start(self) -> None:
#         if self.thread_obj:
#             return
#         self.thread_obj = Thread(
#             target=self.run_tool_in_thread, kwargs={"tool_id": self.tool_id}
#         )
#         self.thread_obj.start()

#     def stop(self) -> None:
#         if self.is_running():
#             self.thread_obj.join()
#             self.thread_obj = None

#     def is_running(self) -> bool:
#         if not self.thread_obj:
#             return False
#         return self.thread_obj.is_alive()

#     def run_tool_in_thread(self, tool_id) -> None:
#         subprocess.run(["python3", self.process_command, tool_id])
