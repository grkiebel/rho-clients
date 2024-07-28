from typing import List
from .model_def import ModelDef, ModelField
from .definitions import FuncDef

""" This module contains classes necessary to generate code
from the information in the FuncDef and ModelDef objects
that have been ."""


class FuncBuilderBase:
    """Creates information needed to generate code for a function
    from the information in the FuncDef object.  Actual code generation
    is implemented by subclasses of this class."""

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

        self.api_return_type = (
            f"List[{self.response_model}]"
            if self.output_is_list
            else self.response_model
        )

        self.api_output_conversion = ""
        if self.output_is_list:
            self.api_output_conversion = (
                f"[{self.response_model}(**item) for item in data]"
            )
        elif self.response_model == "dict":
            self.api_output_conversion = "data"
        else:
            self.api_output_conversion = self.response_model + "(**data)"

        self.api_request_model = (
            f", json=req.model_dump()" if self.request_model else ""
        )

        path_fields: List[str] = [
            f for f in self.path.split("/") if f and not f.startswith("{")
        ]
        self.api_name: str = "_".join(path_fields)
        self.func_type: str = path_fields[1]
        self.cmd_func_name: str = path_fields[-1]
        self.label = " ".join(
            [z.capitalize() for z in [self.path_root, self.cmd_func_name]]
        )

        args_builder = ArgsBuilder(self.base_args, self.request_model, self.func_type)
        self.api_def_args = ", ".join(args_builder.api_def_args)
        self.api_call_args = ", ".join(args_builder.api_call_args)
        self.cmd_args = ", ".join(args_builder.cmd_def_args)

        self.template_tag_values = {
            "<SUMMARY>": self.summary,
            "<PATH>": self.path,
            "<PATH_ROOT>": self.path_root,
            "<FUNC_TYPE>": self.func_type,
            "<HTTP_METHOD>": self.http_method,
            "<ACCESS_FUNC_NAME>": self.api_name,
            "<ACCESS_FUNC_DEF_ARGS>": self.api_def_args,
            "<ACCESS_FUNC_CALLING_ARGS>": self.api_call_args,
            "<ACCESS_FUNC_RETURN_TYPE>": self.api_return_type,
            "<ACCESS_REQUEST_MODEL>": self.api_request_model,
            "<ACCESS_FUNC_OUTPUT_CONVERSION>": self.api_output_conversion,
            "<CMD_FUNC_NAME>": self.cmd_func_name,
            "<CMD_DEF_ARGS>": self.cmd_args,
            "<DISPLAY_LABEL>": self.label,
        }

    def _get_code_from_template(self, template: str) -> str:
        code = template
        for placeholder, value in self.template_tag_values.items():
            code = code.replace(placeholder, value)
        return code

    def dump(self):
        print(f"/n------------------")
        for k, v in self.template_tag_values.items():
            print(f"{k} -> {v}")

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


# --------------------------------------


class ApiFuncBuilder(FuncBuilderBase):
    """Generates code for for an API function from information defined in super class"""

    def __init__(self, func_def: FuncDef):
        super().__init__(func_def)

    def code(self):
        return self._get_code_from_template(self.api_template)

    api_template = f"""
# <SUMMARY>
@handle_exceptions
def <ACCESS_FUNC_NAME>(<ACCESS_FUNC_DEF_ARGS>) -> <ACCESS_FUNC_RETURN_TYPE>:
    url = base_url + f'<PATH>'
    response = requests.<HTTP_METHOD>(url<ACCESS_REQUEST_MODEL>)
    response.raise_for_status()
    data = response.json()
    return <ACCESS_FUNC_OUTPUT_CONVERSION>
"""


# --------------------------------------


class CmdFuncBuilder(FuncBuilderBase):
    """Generates code for a command function from information defined in super class"""

    def __init__(self, func_def: FuncDef):
        super().__init__(func_def)

    def code(self) -> str:
        template = self._get_cmd_code_template()
        return self._get_code_from_template(template)

    def _get_cmd_code_template(self):
        if self.func_type == "create":
            return self.cmd_create_func_template
        return self.cmd_basic_func_template

    @staticmethod
    def shell_definition_code(builders: List[FuncBuilderBase]) -> List[str]:
        """Returns the code that creates a Typer shell for each path root"""
        root_path_set = set([bldr.path_root for bldr in builders])
        root_path_list = sorted(list(root_path_set), reverse=True)
        lines = []
        for root in root_path_list:
            lines.append(f"{root}_app = Typer()")
            lines.append(
                f'make_typer_shell({root}_app, prompt="{root.capitalize()}: ", intro=intro)'
            )
        return lines

    cmd_basic_func_template = f'''
@<PATH_ROOT>_app.command()
def <CMD_FUNC_NAME>(<CMD_DEF_ARGS>):
    """ <SUMMARY> """
    result = apx.<ACCESS_FUNC_NAME>(<ACCESS_FUNC_CALLING_ARGS>)
    display_result(result, "<DISPLAY_LABEL>")
'''

    cmd_create_func_template = f'''
@<PATH_ROOT>_app.command()
def <CMD_FUNC_NAME>(<CMD_DEF_ARGS>):
    """ <SUMMARY> """
    creation_models = hp.make_<ACCESS_FUNC_NAME>_list(num)
    for req in creation_models:
        result = apx.<ACCESS_FUNC_NAME>(<ACCESS_FUNC_CALLING_ARGS>)
        display_result(result, "<DISPLAY_LABEL>")
'''


# --------------------------------------
class ModelBuilder:
    """Creates the code for a Pydantic model
    from the information in the given ModelDef object"""

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
    """Creates (from the given parameters) argument lists
    that are appropriate for both function definition and function invocation"""

    def __init__(self, base_args: List[dict], request_model: str, func_type: str):
        self.api_def_args: List[str] = [f"{p[0]}: {p[1]}" for p in base_args]
        self.api_call_args: List[str] = [p[0] for p in base_args]

        if request_model:
            self.api_def_args.append(f"req: {request_model}")
            self.api_call_args.append("req")

        id_args = [a for a in self.api_call_args if a.endswith("_id")]

        self.cmd_def_args = [f"{a}: IdArg" for a in id_args]
        if func_type == "create":
            self.cmd_def_args.append("num: NumOption")
