import hashlib
import os
import string
import time
import random


def random_password(length: int) -> bytes:
    ascii_lowercase = string.ascii_lowercase.encode()
    return b"".join(bytes(random.choice(ascii_lowercase)) for _ in range(length))


passwords = [random_password(10) for _ in range(10_000)]


def my_hash(password: bytes) -> str:
    salt = os.urandom(16)
    return str(hashlib.scrypt(password, salt=salt, n=2048, p=1, r=8))


start = time.perf_counter()

for pwd in passwords:
    my_hash(pwd)

end = time.perf_counter()
print(end - start)
