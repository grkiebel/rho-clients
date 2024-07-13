from .schema import ApiSchema
from .definitions import Definitions
from .x_file_writers import ApiAccessFileWriter
import argparse


class ApiGenerator:
    def __init__(self, schema_source, output_file):

        self.schema_source = schema_source
        self.output_file = output_file

    def generate_api(self):
        schema = ApiSchema(self.schema_source)
        definitions = Definitions(schema)

        writer = ApiAccessFileWriter(definitions)
        writer.write(self.output_file)


# add a new generator class for each new type of generated file


def main():
    schema_source, output_file = get_args()
    generator = ApiGenerator(schema_source, output_file)
    generator.generate_api()


def get_args():
    parser = argparse.ArgumentParser(description="API Generator")
    parser.add_argument("schema_source", help="Path to the schema source")
    parser.add_argument(
        "-o",
        "--output_file",
        default="rho_clients/access/api_access.py",
        help="Path to the output file",
    )
    args = parser.parse_args()
    return args.schema_source, args.output_file


if __name__ == "__main__":
    # schema_source, output_file = get_args()

    # main(schema_source, output_file)
    main()

    # rho-gen "http://localhost:8080/openapi.json"
