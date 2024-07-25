from typing import List

type_mapping = {
    "string": "str",
    "integer": "int",
    "boolean": "bool",
    "object": "Dict",
    "array": "List",
    "null": "None",
}


def type_map(type: str) -> str:
    return type_mapping.get(type, type)


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
