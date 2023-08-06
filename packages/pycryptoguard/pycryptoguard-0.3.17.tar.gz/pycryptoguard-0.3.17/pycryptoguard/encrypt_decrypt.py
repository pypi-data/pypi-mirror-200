import os
import struct
import random
import hashlib
from Crypto.Cipher import AES

class AESEncryption:
    def __init__(self, password, salt=b'pycryptoguard'):
        self.password = password.encode('utf-8')
        self.salt = salt
        self.key = self.get_key()
        self.block_size = AES.block_size

    def get_key(self):
        hasher = hashlib.sha256(self.password + self.salt)
        return hasher.digest()

    def pad(self, data):
        length = self.block_size - (len(data) % self.block_size)
        return data + (chr(length) * length).encode('utf-8')

    def unpad(self, data):
        return data[:-ord(data[-1])]

    def encrypt(self, inputFile, outputFile=None):
        if not outputFile:
            outputFile = inputFile + '.enc'

        iv = os.urandom(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        with open(inputFile, 'rb') as infile:
            with open(outputFile, 'wb') as outfile:
                outfile.write(struct.pack('<Q', os.path.getsize(inputFile)))
                outfile.write(iv)

                while True:
                    chunk = infile.read(64 * self.block_size)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % self.block_size != 0:
                        chunk = self.pad(chunk)

                    outfile.write(cipher.encrypt(chunk))

        return outputFile

    def decrypt(self, inputFile, outputFile=None):
        if not outputFile:
            outputFile = os.path.splitext(inputFile)[0]

        with open(inputFile, 'rb') as infile:
            original_size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(self.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)

            with open(outputFile, 'wb') as outfile:
                while True:
                    chunk = infile.read(64 * self.block_size)
                    if len(chunk) == 0:
                        break
                    outfile.write(cipher.decrypt(chunk))

                outfile.truncate(original_size)

        return outputFile


def folder(folderPath, password):
    encryption = AESEncryption(password)
    for foldername, subfolders, filenames in os.walk(folderPath):
        for filename in filenames:
            filePath = os.path.join(foldername, filename)
            if filePath.endswith('.enc'):
                continue
            encrypted_file = encryption.encrypt(filePath)
            os.remove(filePath)
            os.rename(encrypted_file, filePath)

        for subfolder in subfolders:
            subfolderPath = os.path.join(foldername, subfolder)
            folder(subfolderPath, password)
