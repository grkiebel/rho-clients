from typing import List
from .schema import type_map


class ModelField:

    def __init__(self, name: str):
        self.name: str = name
        self.types: List[str] = []

    def __str__(self):
        type = " | ".join(self.types)
        return f"{self.name}: {type}"


class ModelDef:
    def __init__(self, model_name: str, schema: dict):
        self.model_name = model_name
        self.fields: List[ModelField] = []

        properties = schema["properties"]
        for prop_name, property in properties.items():
            field = ModelField(prop_name)
            if "type" in property:
                type = type_map(property["type"])
                field.types.append(type)
            elif "anyOf" in property:
                types = [type_map(p["type"]) for p in property["anyOf"]]
                field.types.extend(types)
            else:
                field.types.append("unknown")
            self.fields.append(field)

    def __str__(self):
        output = "\n"
        attributes = vars(self)
        for key, value in attributes.items():
            output += f"\n{key}: {value}"
        return output
