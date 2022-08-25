import random


def base62(inp_text: str):
    CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    BASE = 62

    str_to_bin = "".join(format(ord(i), "b") for i in inp_text)
    hash_num = int(str_to_bin, 2)
    encode = ""
    while hash_num > 0:
        encode += CHARSET[hash_num % BASE]
        hash_num //= BASE

    return encode


def random_key(len: int):
    return random.sample(
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", len
    )


def shorter_url(url: str):
    return base62(random_key(7))
