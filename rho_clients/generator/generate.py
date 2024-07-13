import os
from datetime import datetime
from typing import List
from .builder import FuncBuilder, ModelBuilder, get_cmd_shell_definition_code
from .definitions import Definitions
from .schema import ApiSchema

tmplt_dir = "rho_clients/generator"
output_dir = "rho_clients/generated"


class Generator:
    def __init__(self, source: str = "schema.json"):
        self.schema = ApiSchema(source)
        self.definitions = Definitions(self.schema)
        self.func_builders = [FuncBuilder(fd) for fd in self.definitions.func_defs]
        self.model_builders = [ModelBuilder(md) for md in self.definitions.model_defs]
        self.header = self.get_file_header()
        self.cmd_shell_code = get_cmd_shell_definition_code(self.func_builders)

        self.func_builders.sort(key=lambda fb: fb.func_type)

    def run(self):
        acc_fc = [fd.acc_func_code() for fd in self.func_builders]
        ops_fc = [fd.ops_func_code() for fd in self.func_builders]
        cmd_fc = [fd.cmd_func_code() for fd in self.func_builders]
        model_c = [mb.code() for mb in self.model_builders]

        self.write_x_file("g_api.py", "access_template.py", acc_fc, model_c)
        self.write_x_file("g_ops.py", "ops_template.py", ops_fc, [])
        self.write_x_file("g_cmds.py", "cmd_template.py", cmd_fc, [], cmd=True)

    def get_file_header(self) -> str:
        template_path = os.path.join(tmplt_dir, "header_template.py")
        with open(template_path, "r") as template_file:
            header_template = template_file.read()
            return header_template.replace(
                "<DATE>", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

    def write_x_file(
        self,
        output_file: str,
        template_file: str,
        func_codes: List[str],
        model_codes: List[str],
        cmd: bool = False,
    ):
        template_path = os.path.join(tmplt_dir, template_file)
        with open(template_path, "r") as template:
            template_code = template.read()
        output_file = os.path.join(output_dir, output_file)
        with open(output_file, "w") as file:
            file.write(self.header)
            file.write(template_code)
            if model_codes:
                for model_code in model_codes:
                    file.write(model_code)
                    file.write("\n")
            file.write("\n")

            if cmd:
                file.write(self.cmd_shell_code)
                file.write("\n")

            for func_code in func_codes:
                file.write(func_code)
                file.write("\n")

            file.write("\n")

    def diagnostic(self, file_name: str = "x_diagnostic.txt"):
        diagnostic_file = os.path.join(output_dir, file_name)
        with open(diagnostic_file, "w") as file:
            for fb in self.func_builders:
                file.write("\n-------\n")
                file.write(fb.acc_func_code())
                file.write(fb.ops_func_code())
                file.write(fb.cmd_func_code())


def generate(source: str = "schema.json"):
    Generator(source).run()
