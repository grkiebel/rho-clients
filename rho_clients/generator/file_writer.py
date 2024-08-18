from datetime import datetime
import os
from typing import List


class GeneratedFileWriter:
    """Class to write generated code list to a file"""

    def __init__(self, file_tag: str, code_list: List[str]):
        self.file_tag = file_tag
        self.code_list = code_list

        self.root_dir = "rho_clients"  # TODO: get cwd from os
        self.template_dir = os.path.join(self.root_dir, "generator")
        self.output_dir = os.path.join(self.root_dir, "generated")
        self.template_path = os.path.join(self.template_dir, f"template_{file_tag}.py")
        self.output_file_path = os.path.join(self.output_dir, f"g_{file_tag}.py")
        self.output_file_header = self.get_file_header()
        self.output_file_template_code = self.get_template_code()

        self.assure_folders_exist(self.output_file_path)

    def get_template_code(self) -> str:
        with open(self.template_path, "r") as template:
            return template.read()

    def get_file_header(self) -> str:
        """Get the common header for generated files
        and update date tag with current date/time."""
        template_path = os.path.join(self.template_dir, "template_hdr.py")
        with open(template_path, "r") as template_file:
            header_template = template_file.read()
            return header_template.replace(
                "<DATE>", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

    def assure_folders_exist(self, file_path: str):
        folder_path = os.path.dirname(file_path)
        os.makedirs(folder_path, exist_ok=True)

    def write(self):
        print(f"Writing {self.file_tag} to {self.output_file_path}")

        with open(self.output_file_path, "w") as file:
            file.write(self.output_file_header)
            file.write(self.output_file_template_code)
            for code in self.code_list:
                file.write(code)
                file.write("\n")
            file.write("\n")
