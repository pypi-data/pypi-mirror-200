import logging
from typing import Dict, Any
from math import floor
from random import random
from time import time

B62_ALPHABET_COR = \
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
B62_ALPHABET_MASK = "0123456789abcdefghijklmnopqrstuvwxyz"

def log_exception(source: str, exception: Exception):
    """
    To log exception to console
    usage: log_exception(MyClass, exception_object)
    
    :param source: 
    :param exception: 
    :return: 
    """
    logger = logging.getLogger(source)
    logger.exception(exception)


def log_debug(source: str, data: Any):
    logger = logging.getLogger(source)
    logger.debug(msg=data)


def log_error(source: str, data: Any):
    logger = logging.getLogger(source)
    logger.warning(msg=data)


def log_warning(source: str, data: Any):
    logger = logging.getLogger(source)
    logger.warning(msg=data)


def localize(data_dict: Dict, lang: str) -> str:
    _lang = lang.lower()
    if _lang in data_dict:
        return data_dict[_lang]
    first_lang = list(data_dict.keys())[0]
    log_warning("localize",
                f"Lang: {_lang} not found in ${data_dict}, "
                f"using {first_lang} instead")
    return data_dict[first_lang]

def randomized_ts(masked=True):
    alphabet = B62_ALPHABET_MASK if masked else B62_ALPHABET_COR

    epoch_ms = 1370000000000
    ts_ms = int(time() * 1000)
    relative_ts = ts_ms - epoch_ms

    # if two numbers are generated in the same millisecond,
    # their chances of colliding are one in a million
    random_number = floor(random() * 1000000)
    if random_number > 999999:
        random_number = 999999
    random_ts = int(str(relative_ts) + "%06d" % random_number)
    return base62_encode(random_ts, alphabet)


def randomized_ts_int():
    epoch_ms = 1370000000000
    ts_ms = int(time() * 1000)
    relative_ts = ts_ms - epoch_ms

    # if two numbers are generated in the same millisecond,
    # their chances of colliding are one in a million
    random_number = floor(random() * 1000000)
    if random_number > 999999:
        random_number = 999999
    return int(str(relative_ts) + "%06d" % random_number)


def base62_encode(num, alphabet):
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num //= base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def base62_decode(string, alphabet):
    base = len(alphabet)
    strlen = len(string)
    num = 0
    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1
    return num
