from .generate import Generator
import argparse


# add a new generator class for each new type of generated file


def main():
    schema_source, diagnostic_file = get_args()
    print("schema_source:", schema_source, "\ndiagnostic_file:", diagnostic_file)

    generator = Generator()
    generator.run(source=schema_source, diagnostic=diagnostic_file)
    print("Done")


def get_args():
    parser = argparse.ArgumentParser(description="API Generator")
    parser.add_argument(
        "-s",
        "--schema_source",
        help="Path to the schema source",
        default="http://localhost:8080/openapi.json",
    )
    parser.add_argument(
        "-d",
        "--diagnostic_file",
        action="store_true",
        help="Generate a diagnostic file",
    )
    args = parser.parse_args()
    return args.schema_source, args.diagnostic_file


if __name__ == "__main__":
    main()
