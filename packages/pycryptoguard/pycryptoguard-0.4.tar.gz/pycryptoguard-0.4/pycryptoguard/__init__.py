from Crypto.Cipher import AES
import os


class AESEncryption:

    def __init__(self, key):
        self.key = key.encode("utf-8")
        self.iv = os.urandom(AES.block_size)

    def encrypt_file(self, input_file, output_file):
        with open(input_file, "rb") as infile:
            plaintext = infile.read()

        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        padding = AES.block_size - len(plaintext) % AES.block_size
        plaintext += bytes([padding]) * padding
        ciphertext = cipher.encrypt(plaintext)

        with open(output_file, "wb") as outfile:
            outfile.write(self.iv + ciphertext)

    def decrypt_file(self, input_file, output_file):
        with open(input_file, "rb") as infile:
            ciphertext = infile.read()

        iv = ciphertext[:AES.block_size]
        ciphertext = ciphertext[AES.block_size:]

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)

        padding = plaintext[-1]
        if plaintext[-padding:] != bytes([padding]) * padding:
            raise ValueError("Invalid padding")
        plaintext = plaintext[:-padding]

        with open(output_file, "wb") as outfile:
            outfile.write(plaintext)
