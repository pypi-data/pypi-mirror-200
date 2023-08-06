import os


def check_output_path(output_path):
    # check if output_path exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)
