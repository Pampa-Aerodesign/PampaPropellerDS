import re
import os

def get_model_name(file_path):
    with open(file_path, "r") as file:
        model_line = file.readline()
    file.close()

    model_name = model_line
    model_name = model_name.strip()
    model_name = re.sub(" +", "", model_name)
    return model_name.split("(")[0]


if __name__ == "__main__":
    test_file = os.getcwd()+"/data/raw_files/PER3_4x4E-3.dat"
    print("Model name: ", get_model_name(test_file))