import os
from datetime import datetime
from typing import List
from .builder import FuncBuilder, ModelBuilder, get_cmd_shell_definition_code
from .definitions import Definitions
from .schema import ApiSchema

root_dir = "rho_clients"
tmplt_dir = os.path.join(root_dir, "generator")


def get_file_header() -> str:
    template_path = os.path.join(tmplt_dir, "template_hdr.py")
    with open(template_path, "r") as template_file:
        header_template = template_file.read()
        return header_template.replace(
            "<DATE>", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )


def assure_folders_exist(file_path: str):
    folder_path = os.path.dirname(file_path)
    os.makedirs(folder_path, exist_ok=True)


def write_output_file(key: str, file_info: dict):
    header = get_file_header()

    template_path = file_info["template_file"]

    with open(template_path, "r") as template:
        template_code = template.read()

    output_file = file_info["output_file"]
    assure_folders_exist(output_file)

    print(f"Writing {key} to {output_file}")

    with open(output_file, "w") as file:
        file.write(header)
        file.write(template_code)
        if model_codes := file_info.get("model_code"):
            for model_code in model_codes:
                file.write(model_code)
                file.write("\n")
        file.write("\n")

        if cmd_shell_code := file_info.get("cmd_shell_code"):
            file.write(cmd_shell_code)
            file.write("\n")

        if code_list := file_info.get("code_list"):
            for code in code_list:
                file.write(code)
                file.write("\n")

        file.write("\n")


def write_diagnostic_file(
    bldrs: List[FuncBuilder], file_name: str = "x_diagnostic.txt"
):
    diagnostic_file = os.path.join(root_dir, file_name)
    with open(diagnostic_file, "w") as file:
        for fb in bldrs:
            file.write("\n-------\n")
            file.write(fb.api_func_code())
            file.write(fb.cmd_func_code())


class Generator:
    def __init__(self, source: str = "schema.json"):
        self.schema = ApiSchema(source)
        self.definitions = Definitions(self.schema)
        self.func_builders = [FuncBuilder(fd) for fd in self.definitions.func_defs]
        self.model_builders = [ModelBuilder(md) for md in self.definitions.model_defs]
        self.cmd_shell_code = get_cmd_shell_definition_code(self.func_builders)

        self.func_builders.sort(key=lambda fb: fb.func_type)

        self.file_info = {
            "api_file": {
                "file_name": "g_api.py",
                "template_file": os.path.join(tmplt_dir, "template_api.py"),
                "output_file": os.path.join(root_dir, "api", "g_api.py"),
                "code_list": [fd.api_func_code() for fd in self.func_builders],
                "model_code": [mb.code() for mb in self.model_builders],
            },
            "cmds_file": {
                "file_name": "g_cmds.py",
                "template_file": os.path.join(tmplt_dir, "template_cmd.py"),
                "output_file": os.path.join(root_dir, "cmds", "g_cmds.py"),
                "code_list": [fd.cmd_func_code() for fd in self.func_builders],
                "cmd_shell_code": self.cmd_shell_code,
            },
        }

    def run(self, diagnostic: bool = False):
        for key, file_info in self.file_info.items():
            write_output_file(key, file_info)

        if diagnostic:
            write_diagnostic_file(self.func_builders)


def generate(source: str = "schema.json"):
    Generator(source).run()
