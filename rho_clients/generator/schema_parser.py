if __name__ == "__main__":
    # get all lines from file "api_access.py" that are function definitions
    with open("api_access.py", "r") as file:
        lines = [line.strip() for line in file.readlines() if line.startswith("def")]

        for line in lines:
            # parse the line to extract the function name, function parameters, and return type
            function_name = line.split("def ")[1].split("(")[0]
            parameters = line.split("(")[1].split(")")[0]
            return_type = line.split("-> ")[1].strip() if "->" in line else None
            print(f"function_name: {function_name}")
            print(f"parameters: {parameters}")
            print(f"return_type: {return_type}")
            print()

            # do something with the extracted information
            # ...
            # parse the line to extract the function name, function parameters, and return type

    print("done")
