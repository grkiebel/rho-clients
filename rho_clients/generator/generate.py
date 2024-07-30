import os
from datetime import datetime
from typing import List
from .code_builders import (
    ApiFuncBuilder,
    CmdFuncBuilder,
    FuncBuilderBase,
    ModelBuilder,
)
from .definitions import Definitions
from .schema import ApiSchema

""" This module contains the Generator classes that generates the API, 
command, and diagnostic files"""

root_dir = "rho_clients"
tmplt_dir = os.path.join(root_dir, "generator")


class Generator:
    """Main class to generate the API, command, and diagnostic files"""

    def __init__(self, source: str = "schema.json"):
        self.schema = ApiSchema(source)
        self.definitions = Definitions(self.schema)

    def run(self, diagnostic: bool = False):
        ApiFileGenerator(self.definitions).run()
        CmdFileGenerator(self.definitions).run()
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
        templatePath = os.path.join(tmplt_dir, "template_api.py")
        outputFilePath = os.path.join(root_dir, "api", "g_api.py")
        func_code = [fd.code() for fd in self.func_builders]
        model_code = [mb.code() for mb in self.model_builders]
        code_list = model_code + func_code
        FileOutput("api_file", templatePath, outputFilePath, code_list).write()


class CmdFileGenerator:
    """Generates the command file from the definitions"""

    def __init__(self, definitions: Definitions):
        self.definitions = definitions
        self.func_builders = [CmdFuncBuilder(fd) for fd in self.definitions.func_defs]
        self.cs_builders = CmdFuncBuilder.shell_definition_code(self.func_builders)

        self.func_builders.sort(key=lambda fb: fb.func_type)

    def run(self):
        templatePath = os.path.join(tmplt_dir, "template_cmd.py")
        outputFilePath = os.path.join(root_dir, "cmds", "g_cmds.py")
        shell_def_code = CmdFuncBuilder.shell_definition_code(self.func_builders)
        func_code = [fd.code() for fd in self.func_builders]
        code_list = shell_def_code + func_code
        FileOutput("cmds_file", templatePath, outputFilePath, code_list).write()


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

        outputFilePath = os.path.join(root_dir, "x_diagnostic.txt")
        templatePath = os.path.join(tmplt_dir, "template_diagnostic.py")
        FileOutput("diagnostic_file", templatePath, outputFilePath, code_list).write()


class FileOutput:
    """Class to write generated code list to a file"""

    def __init__(
        self, key: str, template_path: str, output_file: str, code_list: List[str]
    ):
        self.tmplt_dir = os.path.join(root_dir, "generator")
        self.key = key
        self.template_path = template_path
        self.output_file = output_file
        self.code_list = code_list

        self.header = self.get_file_header()
        self.assure_folders_exist(output_file)
        with open(template_path, "r") as template:
            self.template_code = template.read()

    def get_file_header(self) -> str:
        """Get the common header for generated files
        and update date tag with current date/time."""
        template_path = os.path.join(self.tmplt_dir, "template_hdr.py")
        with open(template_path, "r") as template_file:
            header_template = template_file.read()
            return header_template.replace(
                "<DATE>", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

    def assure_folders_exist(self, file_path: str):
        folder_path = os.path.dirname(file_path)
        os.makedirs(folder_path, exist_ok=True)

    def write(self):
        print(f"Writing {self.key} to {self.output_file}")

        with open(self.output_file, "w") as file:
            file.write(self.header)
            file.write(self.template_code)
            for code in self.code_list:
                file.write(code)
                file.write("\n")
            file.write("\n")
