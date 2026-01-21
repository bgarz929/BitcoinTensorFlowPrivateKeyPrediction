import numpy as np


def intFromBytes(byteS):
    # unchanged logic
    return int.from_bytes(byteS, byteorder="big")


def binArray2float32array(bin_array):
    # ensure float32 output (TensorFlow safe)
    return np.asarray(bin_array, dtype=np.float32)


def float_array_to_hex(array, fill):
    # convert float into 0 or 1 depending on > 0.5
    binary_string = ''.join(
        '1' if bit > 0.5 else '0'
        for bit in array
    )

    # fill array with leading zeros
    return hex(int(binary_string, 2))[2:].zfill(fill)


def convert_to_binary(element, bits):
    # remove '0b', convert number to binary string and fill with leading zeros
    binary = format(element, f'0{bits}b')

    # convert binary string into list of integer
    return [int(bit) for bit in binary]


def convert_to_binary_arrays(given_array, bits):
    # faster & deterministic
    return [
        convert_to_binary(element, bits)
        for element in given_array
    ]
