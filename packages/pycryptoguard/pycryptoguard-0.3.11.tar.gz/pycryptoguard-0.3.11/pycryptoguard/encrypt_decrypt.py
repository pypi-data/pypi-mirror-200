import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import getpass


class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, filename):
        chunksize = 64 * 1024
        outputFolder = "enc_" + os.path.dirname(filename)
        os.makedirs(outputFolder, exist_ok=True)  # create folder if it doesn't exist
        outputFile = os.path.join(outputFolder, os.path.basename(filename))
        filesize = str(os.path.getsize(filename)).zfill(16)
        IV = Random.new().read(16)

        encryptor = AES.new(self.key, AES.MODE_CBC, IV)

        with open(filename, 'rb') as infile:
            with open(outputFile, 'wb') as outfile:
                outfile.write(filesize.encode('utf-8'))
                outfile.write(IV)

                while True:
                    chunk = infile.read(chunksize)

                    if len(chunk) == 0:
                        break

                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - (len(chunk) % 16))

                    outfile.write(encryptor.encrypt(chunk))

        return outputFile

    def decrypt(self, filename):
        chunksize = 64 * 1024
        outputFolder = os.path.dirname(filename)[4:]
        os.makedirs(outputFolder, exist_ok=True)  # create folder if it doesn't exist
        outputFile = os.path.join(outputFolder, os.path.basename(filename)[4:])

        with open(filename, 'rb') as infile:
            filesize = int(infile.read(16))
            IV = infile.read(16)

            decryptor = AES.new(self.key, AES.MODE_CBC, IV)

            with open(outputFile, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)

                    if len(chunk) == 0:
                        break

                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(filesize)

        return outputFile


def get_key(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()


class AESEncryption:
    def __init__(self, password):
        self.key = get_key(password)

    def file(self, filename):
        cipher = AESCipher(self.key)
        encrypted_file = cipher.encrypt(filename)
        print(f"File '{filename}' encrypted as '{encrypted_file}'")

    def folder(self, foldername):
        cipher = AESCipher(self.key)

        for root, dirs, files in os.walk(foldername):
            for filename in files:
                filepath = os.path.join(root, filename)
                encrypted_file = cipher.encrypt(filepath)
                print(f"File '{filepath}' encrypted as '{encrypted_file}'")

    def get_key(self):
        return self.key


class AESDecryption:
    def __init__(self, password):
        self.key = get_key(password)

    def file(self, filename):
        cipher = AESCipher(self.key)
        decrypted_file = cipher.decrypt(filename)
        print(f"File '{filename}' decrypted as '{decrypted_file}'")

    def folder(self, foldername):
        cipher = AESCipher(self.key)

        for root, dirs, files in os.walk(foldername):
            for file in files:
                filepath = os.path.join(root, file)
                decrypted_file = cipher.decrypt(filepath)
                print(f"File '{filepath}' decrypted as '{decrypted_file}'")

    def get_key(self):
        return self.key
