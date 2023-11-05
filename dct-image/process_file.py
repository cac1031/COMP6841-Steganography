#!/usr/bin/env python3
import os

BLOCKSIZE = 8

def make_file_path(input_path):
    '''
    Take in input file path and make an output path to store stego image
    '''
    path_components = input_path.rsplit('.', 1)

    extension = ''
    if len(path_components) > 1:
        extension = '.' + path_components[-1]
        path_components = ''.join(path_components[:-1])
    else:
        path_components = ''.join(path_components)

    i = 1
    output_path = ''
    while True:
        output_path = f'{path_components}{i}{extension}'
        
        if not os.path.exists(output_path):
            return output_path
        i += 1


def file_to_binstring(file_path):
    '''
    Convert a file to a binary string
    '''
    try:
        with open(file_path, "rb") as file:
            bin_data = file.read()
            binstring = ''.join(format(byte, '08b') for byte in bin_data)
            return binstring
    except FileNotFoundError:
        return None


def binstring_to_file(bin_data, output_file_path):
    '''
    Convert a binary string and write it to a file
    '''
    try:
        file_bytes = bytearray(int(bin_data[i:i + BLOCKSIZE], 2) for i in range(0, len(bin_data), BLOCKSIZE))
        
        with open(output_file_path, 'wb') as output_file:
            output_file.write(file_bytes)
    except Exception as e:
        print(f"Error: {e}")
