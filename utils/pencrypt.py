# AES 256 encryption/decryption using pycrypto library

import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

import utils.config as cf

# BLOCK_SIZE = 16
# pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
# unpad = lambda s: s[:-ord(s[len(s) - 1:])]

# password = input("Enter encryption password: ")


def get_private_key(keyword):
    salt = b"this is a salt"
    kdf = PBKDF2(keyword, salt, 64, 1000)
    key = kdf[:32]
    return key


def encrypt(raw, keyword):
    private_key = get_private_key(keyword)
    raw = pad(bytes(raw, "utf-8"), 16)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, keyword):
    data = base64.b64decode(enc)
    key = get_private_key(keyword)
    iv = data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return bytes.decode(unpad(cipher.decrypt(data), 16)[16:])



# print(encrypt("siddhip", cv.SECRET_KEY))
# print(decrypt("79xZK+JdT0TOlMFwmNA2DQRGE3womifxZeq4OgkJwG0=", cv.SECRET_KEY))