import os
from datetime import datetime
from typing import List
from .code_builders import ApiFuncBuilder, CmdFuncBuilder, ModelBuilder
from .definitions import Definitions, get_definitions
from .file_writer import GeneratedFileWriter

""" This module contains the Generator classes that generates the API, 
command, and diagnostic files"""


class Generator:
    """Main class to generate the API, command, and diagnostic files"""

    def run(self, source: str = "schema.json", diagnostic: bool = False):
        definitions = get_definitions(source)

        ApiFileGenerator(definitions).run()
        CmdFileGenerator(definitions).run()
        if diagnostic:
            DiagnosticFileGenerator(self.definitions).run()


class ApiFileGenerator:
    """Generates the API file from the definitions"""

    def __init__(self, definitions: Definitions):
        self.definitions = definitions
        self.func_builders = [ApiFuncBuilder(fd) for fd in self.definitions.func_defs]
        self.model_builders = [ModelBuilder(md) for md in self.definitions.model_defs]

        self.func_builders.sort(key=lambda fb: fb.func_type)

    def run(self):
        func_code = [fd.code() for fd in self.func_builders]
        model_code = [mb.code() for mb in self.model_builders]
        code_list = model_code + func_code
        GeneratedFileWriter("api", code_list).write()


class CmdFileGenerator:
    """Generates the command file from the definitions"""

    def __init__(self, definitions: Definitions):
        self.definitions = definitions
        self.func_builders = [CmdFuncBuilder(fd) for fd in self.definitions.func_defs]
        self.cs_builders = CmdFuncBuilder.shell_definition_code(self.func_builders)

        self.func_builders.sort(key=lambda fb: fb.func_type)

    def run(self):
        shell_def_code = CmdFuncBuilder.shell_definition_code(self.func_builders)
        func_code = [fd.code() for fd in self.func_builders]
        code_list = shell_def_code + func_code
        GeneratedFileWriter("cmds", code_list).write()


class DiagnosticFileGenerator:
    """Generates the diagnostic file from the definitions"""

    def __init__(self, definitions: Definitions):
        self.definitions = definitions

    def run(self):
        code_list: List[str] = []
        for fd in self.definitions:
            api_func_code = ApiFuncBuilder(fd).code()
            cmd_func_code = CmdFuncBuilder(fd).code()
            code_list.append("\n-------\n")
            code_list.append(api_func_code())
            code_list.append(cmd_func_code())

        GeneratedFileWriter("diagnostic", code_list).write()
