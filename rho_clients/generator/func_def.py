from typing import List
from .schema import type_map


class Parameter:
    def __init__(self, parameter: dict):
        self.name = parameter.get("name")
        self.in_ = parameter.get("in")
        self.required = parameter.get("required")
        type = parameter.get("schema").get("type")
        self.type = type_map(type)

    def __str__(self):
        output = "\n"
        attributes = vars(self)
        for key, value in attributes.items():
            output += f"\n{key}: {value}"
        return output


class FuncDef:
    def __init__(self, path: str, method: str, method_data: dict):
        self.path = path
        self.summary = method_data.get("summary")
        self.method: str = method
        self.operationId: str = method_data["operationId"]
        self.request_model: str = None
        self.response_model = None
        self.response_type = None
        self.parameters: List[Parameter] = []

        if request := method_data.get("requestBody"):
            self.process_request_body_section(request)

        if parameters := method_data.get("parameters"):
            self.process_parameters_section(parameters)

        for key, value in method_data["responses"].items():
            if not key == "200":  # only interested in 200 responses
                continue
            self.process_response_section(value)

    def process_request_body_section(self, request: dict):
        if ref := request.get("content").get("application/json").get("schema"):
            ref_path = ref.get("$ref")
            self.request_model = self.extract_class_name(ref_path)

    def process_parameters_section(self, parameters):
        for parameter in parameters:
            self.parameters.append(Parameter(parameter))

    def process_response_section(self, value: dict):
        schema = value.get("content").get("application/json").get("schema")
        self.type = schema.get("type")
        if self.type == "object":
            self.response_model = "dict"
        else:
            self.response_model = self.extract_model(schema)
        # print(f"{self.operationId} -> Type: {self.type},  Model:{self.response_model}")

    def extract_class_name(self, value: str):
        return value.split("/")[-1]

    def extract_model(self, schema: dict):
        ref = schema.get("$ref", None)
        ref_path = schema.get("items", {}).get("$ref", None)
        if ref:
            return self.extract_class_name(ref)
        if ref_path:
            return self.extract_class_name(ref_path)
        return None

    def __str__(self):
        output = "\n"
        attributes = vars(self)
        for key, value in attributes.items():
            if key == "parameters":
                output += "\nparameters:"
                for param in value:
                    output += str(param)
            else:
                output += f"\n{key}: {value}"
        return output
