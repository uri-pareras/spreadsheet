"""
This file contains utility functions.
"""


def base26_to_int(s):
    """
    This function converts a string to an integer in base-26.
    """
    result_int = 0
    for c in s:
        result_int = result_int * 26 + ord(c) - ord('A') + 1
    return result_int - 1  # Subtract 1 for 0-indexing


def int_to_base26(num):
    """
    This function converts an integer to a string in base-26.
    """
    result_b26 = ''
    while num >= 0:
        result_b26 = chr(num % 26 + ord('A')) + result_b26
        num //= 26
        num -= 1  # Subtract 1 for 0-indexing
    return result_b26
