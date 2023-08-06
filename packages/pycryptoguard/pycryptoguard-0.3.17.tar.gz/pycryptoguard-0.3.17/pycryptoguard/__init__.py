from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256

import os


class AESEncryption:
    def __init__(self, password, salt=b''):
        self.salt = salt
        self.key = get_key(password, salt)
        self.block_size = AES.block_size

    def encrypt(self, inputFile, outputFile=None):
        if outputFile is None:
            outputFile = 'enc_' + inputFile

        with open(inputFile, 'rb') as infile:
            data = infile.read()

        cipher = AES.new(self.key, AES.MODE_CBC)
        iv = cipher.iv
        encrypted_data = cipher.encrypt(pad(data, self.block_size))

        with open(outputFile, 'wb') as outfile:
            outfile.write(iv)
            outfile.write(encrypted_data)

    def decrypt(self, inputFile, outputFile=None):
        if outputFile is None:
            outputFile = 'dec_' + os.path.splitext(inputFile)[0]

        with open(inputFile, 'rb') as infile:
            iv = infile.read(self.block_size)
            encrypted_data = infile.read()

        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), self.block_size)

        with open(outputFile, 'wb') as outfile:
            outfile.write(decrypted_data)


def get_key(password, salt=b''):
    hasher = SHA256.new(password.encode('utf-8') + salt)
    key = hasher.digest()
    return key

