import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


class AESEncryption:
    def __init__(self, password, salt=b'pycryptoguard'):
        self.key = get_key(password, salt)
        self.bs = AES.block_size

    def encrypt_file(self, input_file, output_file):
        iv = os.urandom(self.bs)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        with open(input_file, 'rb') as infile:
            with open(output_file, 'wb') as outfile:
                outfile.write(iv)
                while True:
                    chunk = infile.read(64 * self.bs)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % self.bs != 0:
                        chunk += b' ' * (self.bs - len(chunk) % self.bs)
                    outfile.write(cipher.encrypt(chunk))

    def decrypt_file(self, input_file, output_file):
        with open(input_file, 'rb') as infile:
            iv = infile.read(self.bs)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            with open(output_file, 'wb') as outfile:
                while True:
                    chunk = infile.read(64 * self.bs)
                    if len(chunk) == 0:
                        break
                    outfile.write(cipher.decrypt(chunk))

    def encrypt_folder(self, input_folder, output_folder):
        for dirpath, dirnames, filenames in os.walk(input_folder):
            for filename in filenames:
                input_file = os.path.join(dirpath, filename)
                output_file = os.path.join(output_folder, os.path.relpath(input_file, input_folder))
                self.encrypt_file(input_file, output_file)

    def decrypt_folder(self, input_folder, output_folder):
        for dirpath, dirnames, filenames in os.walk(input_folder):
            for filename in filenames:
                input_file = os.path.join(dirpath, filename)
                output_file = os.path.join(output_folder, os.path.relpath(input_file, input_folder))
                self.decrypt_file(input_file, output_file)

def get_key(password, salt):
    hasher = SHA256.new(password.encode('utf-8') + salt)
    key = hasher.digest()
    return key
