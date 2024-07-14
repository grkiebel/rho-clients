from .schema import ApiSchema
from .definitions import Definitions
from .generate import Generator
import argparse


# add a new generator class for each new type of generated file


def main():
    schema_source, output_file = get_args()
    generator = Generator(source="http://localhost:8080/openapi.json")
    generator.run()
    generator.write_diagnostic_file()


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
    main()
