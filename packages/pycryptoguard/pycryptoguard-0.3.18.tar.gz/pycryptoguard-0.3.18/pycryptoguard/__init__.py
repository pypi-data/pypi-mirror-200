from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import os


class AESEncryption:
    def __init__(self, password, salt=b'salt_'):
        self.key = self.get_key(password, salt)

    def get_key(self, password, salt):
        hasher = SHA256.new(password.encode('utf-8') + salt)
        return hasher.digest()

    def encrypt(self, inputFile, outputFile=None):
        if not outputFile:
            outputFile = inputFile + ".enc"

        chunk_size = 64 * 1024
        file_size = str(os.path.getsize(inputFile)).zfill(16).encode()
        iv = Random.new().read(16)

        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        with open(inputFile, 'rb') as infile:
            with open(outputFile, 'wb') as outfile:
                outfile.write(file_size)
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunk_size)

                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - (len(chunk) % 16))

                    outfile.write(cipher.encrypt(chunk))

    def decrypt(self, inputFile, outputFile=None):
        if not outputFile:
            outputFile = inputFile[:-4]

        chunk_size = 64 * 1024
        with open(inputFile, 'rb') as infile:
            file_size = int(infile.read(16))
            iv = infile.read(16)

            cipher = AES.new(self.key, AES.MODE_CBC, iv)

            with open(outputFile, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunk_size)

                    if len(chunk) == 0:
                        break

                    outfile.write(cipher.decrypt(chunk))

                outfile.truncate(file_size)

    def folder(self, inputFolder, outputFolder=None):
        if not outputFolder:
            outputFolder = 'enc_' + inputFolder

        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        for item in os.listdir(inputFolder):
            path = os.path.join(inputFolder, item)

            if os.path.isdir(path):
                self.folder(path, os.path.join(outputFolder, item))
            else:
                self.encrypt(path, os.path.join(outputFolder, item + '.enc'))

    def decrypt_folder(self, inputFolder, outputFolder=None):
        if not outputFolder:
            outputFolder = inputFolder[4:]

        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        for item in os.listdir(inputFolder):
            path = os.path.join(inputFolder, item)

            if os.path.isdir(path):
                self.decrypt_folder(path, os.path.join(outputFolder, item))
            else:
                self.decrypt(path, os.path.join(outputFolder, item[:-4]))
