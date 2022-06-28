import logging
import re


def _apc_to_csv_buffer(file_lines: list):
    """Will convert APC data to a csv file.

    Args:
        file_lines (list): List of lines from the APC file.

    Returns:
        str: String with csv data.
    """
    buffer = ""
    searching_headers = True
    searching_units = False
    index = 0
    for line in file_lines:
        if re.search("PROP RPM", line):
            rpm = line.strip()
            rpm = re.sub("  +", "", rpm)
            rpm = re.sub("[^0-9]", "", rpm)

        if (not re.search(r"[a-zA-z]", line)) and (not line.isspace()):
            data_line = line.strip()
            data_line = re.sub(" +", ",", data_line)

            buffer = buffer + f"{index}," + data_line + "," + rpm + "\n"
            index += 1

        if (
            (not re.search(r"[0-9\(\)\:]", line))
            and (not line.isspace())
            and searching_headers
        ):
            headers_line = line.strip()
            headers_line = re.sub(" +", ",", headers_line)

            buffer = buffer + "," + headers_line + "," + "RPM" + "\n"
            searching_headers = False
            searching_units = True
            continue

        if searching_units:
            units_line = line.strip()
            units_line = re.sub("  +", ",", units_line)

            if len(headers_line.split(",")) != len(units_line.split(",")):
                units_line = units_line[:18] + "-,-,-," + units_line[18:]

            buffer = buffer + f"{index}," + units_line + "," + "RPM" + "\n"
            index += 1
            searching_units = False

    return buffer


def get_model_name(filepath_or_buffer: str) -> str:
    """Will get the model name from the APC file.

    Args:
        filepath_or_buffer (str): Filepath or buffer with APC data.

    Returns:
        str: Model name.
    """
    try:
        if type(filepath_or_buffer) is str:
            with open(filepath_or_buffer) as file:
                file_lines = file.readlines()
            file.close()
        else:
            file_lines = filepath_or_buffer.readlines()
    except Exception as e:
        logging.error(f"Fail reading {filepath_or_buffer}\n{e}")

    line = file_lines[0]
    line = line.strip()
    line = re.sub(" +", "", line)
    return line.split("(")[0]


def apc_to_csv(
    raw_filepath_or_buffer: str,
    csv_filepath: str,
):
    """Will convert a raw APC data to a csv file.

    Args:
        raw_filepath_or_buffer (str): Filepath or buffer with raw APC data.
        csv_filepath (str, optional): Filepath to save the csv file.
    """

    try:
        if type(raw_filepath_or_buffer) is str:
            with open(raw_filepath_or_buffer) as file:
                file_lines = file.readlines()
            file.close()
        else:
            file_lines = raw_filepath_or_buffer.readlines()
    except Exception as e:
        logging.error(f"Fail reading {raw_filepath_or_buffer}\n{e}")

    buffer = _apc_to_csv_buffer(file_lines)

    try:
        with open(csv_filepath, "w") as file:
            file.write(buffer)
        file.close()
    except Exception as e:
        logging.error(f"Fail writing {csv_filepath}\n{e}")
