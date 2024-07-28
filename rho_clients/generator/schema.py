import json
import requests


class ApiSchema:
    """Class to obtain and store the schema of the API
    either from a file or directly from the rho-service."""

    def __init__(self, source: str):
        self.schema = self.obtain_schema(source)
        self.model_specs: dict = self.extract_model_schemas()
        self.path_specs: dict = self.extract_url_paths_schemas()

    def obtain_schema(self, source: str) -> dict:
        """Determine if the schema source is a URL or file name
        and obtain the schema."""
        if source.startswith("http://") or source.startswith("https://"):
            return self.obtain_schema_from_url(source)
        else:
            return self.obtain_schema_from_file(source)

    def obtain_schema_from_url(self, source: str) -> dict:
        try:
            response = requests.get(source)
            response.raise_for_status()
            schema: dict = response.json()
            return schema
        except requests.exceptions.RequestException as e:
            print("Failed to retrieve data from the URL:", str(e))
            return {}

    def obtain_schema_from_file(self, source: str) -> dict:
        try:
            with open(source, "r") as file:
                schema: dict = json.load(file)
            return schema
        except FileNotFoundError:
            print("File not found.")
            return {}

    def extract_url_paths_schemas(self):
        """Extract the URL paths and their schemas from the schema."""
        return self.schema["paths"] if self.schema else {}

    def extract_model_schemas(self):
        """Extract the model schemas from the schema."""
        return self.schema["components"]["schemas"] if self.schema else {}
