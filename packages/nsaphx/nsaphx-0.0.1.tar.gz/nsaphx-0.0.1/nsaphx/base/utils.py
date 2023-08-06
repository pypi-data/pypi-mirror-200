import random
import numpy as np
import pandas as pd
import os


from nsaphx.log import LOGGER


def nested_get(d, keys, default=None):
    """ Get a value from a nested dictionary.

    Parameters
    ----------
    d : dict
        The dictionary to search.
    keys : list
        The list of keys to search for.

    Returns
    -------
    value : object
        The value of the key if found, otherwise None.
    """
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d

def human_readible_size(nbytes):
    """
    Convert a number of bytes to a human readable string. 
    """
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1

    return f"{nbytes:.2f} {suffixes[i]}"


def check_instruction_keys(keys, instruction):
    missing_keys = [key for key in keys if key not in instruction.keys()]
    if len(missing_keys) > 0:
        raise ValueError(f"Missing keys: {missing_keys} in the instruction.")
