import re

def get_model_name(file_path):
    with open(file_path, "r") as file:
        file_lines = file.readlines(1)
    file.close()

    line = file_lines[0]
    line = line.strip()
    line = re.sub(" +", "", line)
    return line.split("(")[0]