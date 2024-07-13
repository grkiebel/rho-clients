from ast import arg
import cmd
from typing import List
from .model_def import ModelDef, ModelField
from .definitions import FuncDef


# --------------------------------------
class ModelBuilder:
    indent = "    "

    def __init__(self, model_def: ModelDef):
        self.model_name: str = model_def.model_name
        self.fields: List[ModelField] = model_def.fields

    def code(self):
        code_block = f"class {self.model_name}(BaseModel):\n"
        for field in self.fields:
            field_code = f"{self.indent}{str(field)}\n"
            code_block += field_code
        return code_block


class ArgsBuilder:
    def __init__(self, base_args: List[dict], request_model: str, func_type: str):
        self.acc_def_args: List[str] = [f"{p[0]}: {p[1]}" for p in base_args]
        self.acc_call_args: List[str] = [p[0] for p in base_args]

        self.ops_def_args: List[str] = [a for a in self.acc_def_args]
        self.ops_call_args: List[str] = [a for a in self.acc_call_args]

        if request_model:
            self.acc_def_args.append(f"req: {request_model}")
            self.acc_call_args.append("req")

        id_args = [a for a in self.acc_call_args if a.endswith("_id")]

        self.cmd_def_args = [f"{a}: IdArg" for a in id_args]
        if func_type == "create":
            self.cmd_def_args.append("num: NumOption")
            self.ops_def_args.append("num: int")
            self.ops_call_args.append("num")


class FuncBuilderBase:
    """Creates information needed to generate code for a function"""

    def __init__(self, func_def: FuncDef):
        self.func_def: FuncDef = func_def

        self.summary: str = func_def.summary
        self.http_method: str = func_def.method
        self.path: str = func_def.path
        self.request_model: str = func_def.request_model
        self.response_type = self.func_def.response_type
        self.response_model = self.func_def.response_model
        self.path_root: str = self.path.split("/")[1]
        self.output_is_list = self.func_def.type == "array"

        self.base_args: List[dict] = (
            [(param.name, param.type) for param in self.func_def.parameters]
            if self.func_def.parameters
            else []
        )

        self.acc_return_type = (
            f"List[{self.response_model}]"
            if self.output_is_list
            else self.response_model
        )

        self.acc_output_conversion = ""
        if self.output_is_list:
            self.acc_output_conversion = (
                f"[{self.response_model}(**item) for item in data]"
            )
        elif self.response_model == "dict":
            self.acc_output_conversion = "data"
        else:
            self.acc_output_conversion = self.response_model + "(**data)"

        self.acc_request_model = (
            f", json=req.model_dump()" if self.request_model else ""
        )

        path_fields: List[str] = [
            f for f in self.path.split("/") if f and not f.startswith("{")
        ]
        self.acc_name: str = "_".join(path_fields)
        self.ops_func_name: str = "_".join(path_fields)
        self.func_type: str = path_fields[1]

        args_builder = ArgsBuilder(self.base_args, self.request_model, self.func_type)
        self.acc_def_args = ", ".join(args_builder.acc_def_args)
        self.acc_call_args = ", ".join(args_builder.acc_call_args)
        self.ops_func_def_args = ", ".join(args_builder.ops_def_args)
        self.ops_func_call_args = ", ".join(args_builder.ops_call_args)
        self.cmd_args = ", ".join(args_builder.cmd_def_args)

        self.template_tag_values = {
            "<SUMMARY>": self.summary,
            "<ACCESS_FUNC_NAME>": self.acc_name,
            "<ACCESS_FUNC_DEF_ARGS>": self.acc_def_args,
            "<ACCESS_FUNC_CALLING_ARGS>": self.acc_call_args,
            "<ACCESS_FUNC_RETURN_TYPE>": self.acc_return_type,
            "<PATH>": self.path,
            "<HTTP_METHOD>": self.http_method,
            "<ACCESS_REQUEST_MODEL>": self.acc_request_model,
            "<ACCESS_FUNC_OUTPUT_CONVERSION>": self.acc_output_conversion,
            "<PATH_ROOT>": self.path_root,
            "<FUNC_TYPE>": self.func_type,
            "<OPS_FUNC_NAME>": self.ops_func_name,
            "<OPS_FUNC_DEF_ARGS>": self.ops_func_def_args,
            "<OPS_FUNC_CALLING_ARGS>": self.ops_func_call_args,
            "<CMD_DEF_ARGS>": self.cmd_args,
        }


# --------------------------------------

acc_template = f"""
# <SUMMARY>
@handle_exceptions
def <ACCESS_FUNC_NAME>(<ACCESS_FUNC_DEF_ARGS>) -> <ACCESS_FUNC_RETURN_TYPE>:
    url = base_url + '<PATH>'
    response = requests.<HTTP_METHOD>(url<ACCESS_REQUEST_MODEL>)
    response.raise_for_status()
    data = response.json()
    return <ACCESS_FUNC_OUTPUT_CONVERSION>
"""


ops_basic_func_template = f"""
# <SUMMARY>
def <OPS_FUNC_NAME>(<ACCESS_FUNC_DEF_ARGS>):
    result = apx.<ACCESS_FUNC_NAME>(<ACCESS_FUNC_CALLING_ARGS>)
    display_result(result)
"""

ops_create_func_templete = f"""
# <SUMMARY>
def <OPS_FUNC_NAME>(<OPS_FUNC_DEF_ARGS>):
    creation_list = sim.make_<OPS_FUNC_NAME>_list(num)
    for item in creation_list:
        result = apx.<ACCESS_FUNC_NAME>(item)
        display_result(result)
"""


cmd_func_template = f'''
@<PATH_ROOT>_app.command()
def <FUNC_TYPE>(<CMD_DEF_ARGS>):
    """ <SUMMARY> """
    ops.<OPS_FUNC_NAME>(<OPS_FUNC_CALLING_ARGS>)
'''

# --------------------------------------


class FuncBuilder(FuncBuilderBase):
    """Generates code for function group from information defined in super class"""

    def __init__(self, func_def: FuncDef):
        super().__init__(func_def)

    def acc_func_code(self):
        return self._get_code_from_template(acc_template)

    def ops_func_code(self) -> str:
        template = self._get_ops_code_template()
        return self._get_code_from_template(template)

    def cmd_func_code(self) -> str:
        return self._get_code_from_template(cmd_func_template)

    def __str__(self):
        items = [
            f"\nSummary -> {self.summary}",
            f"Method -> {self.http_method}",
            f"Path -> {self.path}",
            f"Request Model -> {self.request_model}",
            f"Base Args -> {self.base_args}",
            f"Response Model -> {self.response_model}",
            f"Output is List -> {self.output_is_list}",
        ]
        return "\n".join(items)

    def _get_ops_code_template(self):
        if self.func_type == "create":
            return ops_create_func_templete
        return ops_basic_func_template

    def _get_code_from_template(self, template: str):
        code = template
        for placeholder, value in self.template_tag_values.items():
            code = code.replace(placeholder, value)
        return code


# --------------------------------------


def get_cmd_shell_definition_code(builders: List[FuncBuilder]) -> str:
    """Returns the code that creates a Typer shell for each path root"""
    root_path_set = set([bldr.path_root for bldr in builders])
    root_path_list = sorted(list(root_path_set), reverse=True)
    lines = []
    for root in root_path_list:
        lines.append(f"{root}_app = Typer()")
        lines.append(
            f'make_typer_shell({root}_app, prompt="{root.capitalize()}: ", intro=intro)'
        )
    return "\n".join(lines)
