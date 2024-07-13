from typing import List
from .schema import ApiSchema
from .func_def import FuncDef
from .model_def import ModelDef


class Definitions:
    def __init__(self, schema: ApiSchema):

        self.model_defs: List[ModelDef] = []
        for model_name, model_specs in schema.model_specs.items():
            model_def = ModelDef(model_name, model_specs)
            self.model_defs.append(model_def)

        self.func_defs: List[FuncDef] = []
        for path, path_schema in schema.path_specs.items():
            for method, method_data in path_schema.items():
                func_def = FuncDef(path, method, method_data)
                self.func_defs.append(func_def)
