import os


def convert_file_to_binary(file_path):
    # Open the input file in binary mode and read its contents
    with open(file_path, "rb") as input_file:
        data = input_file.read()

    # Construct the output file path by replacing the original extension with .bin
    output_file_path = os.path.splitext(file_path)[0] + ".bin"

    # Open the output file in binary mode and write the data to it
    with open(output_file_path, "wb") as output_file:
        output_file.write(data)

    return output_file_path


def binary_to_file(binary_file_path, output_extension=None):
    # Open the binary file in binary mode and read its contents
    with open(binary_file_path, "rb") as binary_file:
        data = binary_file.read()

    # Construct the output file path by replacing the .bin extension with the specified output extension
    if output_extension is None:
        output_extension = os.path.splitext(binary_file_path)[1][1:]
    output_file_path = os.path.splitext(binary_file_path)[0] + "." + output_extension

    # Open the output file in binary mode and write the data to it
    with open(output_file_path, "wb") as output_file:
        output_file.write(data)

    return output_file_path