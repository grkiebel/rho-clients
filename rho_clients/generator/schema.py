import json
import requests


class ApiSchema:
    def __init__(self, source: str):
        self.schema = self.obtain_schema(source)
        self.model_specs: dict = (
            self.schema["components"]["schemas"] if self.schema else {}
        )
        self.path_specs: dict = self.schema["paths"] if self.schema else {}

    def obtain_schema(self, source: str) -> dict:
        if source.startswith("http://") or source.startswith("https://"):
            # Source is a URL
            try:
                response = requests.get(source)
                response.raise_for_status()
                schema: dict = response.json()
                return schema
            except requests.exceptions.RequestException as e:
                print("Failed to retrieve data from the URL:", str(e))
                return {}
        else:
            # Source is a file path
            try:
                with open(source, "r") as file:
                    schema: dict = json.load(file)
                return schema
            except FileNotFoundError:
                print("File not found.")
                return {}
