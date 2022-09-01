import random

class ShortLink():
    def __init__(self):
        self._CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        
    def _base62(self, inp_text: str):
        BASE = 62

        str_to_bin = "".join(format(ord(i), "b") for i in inp_text)
        hash_num = int(str_to_bin, 2)
        encode = ""
        while hash_num > 0:
            encode += self.CHARSET[hash_num % BASE]
            hash_num //= BASE

        return encode


    def random_key(self, len: int):
        return random.sample(
            self.CHARSET, len
        )

    @staticmethod
    def shorter_url(self, url: str):
        return self._base62(self.random_key(7))
