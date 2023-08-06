from Crypto.Cipher import AES
import os


class PyEncrypt:
    @staticmethod
    def aes_encrypt(file_path):
        key = b'0123456789abcdef'
        iv = b'fedcba9876543210'

        with open(file_path, 'rb') as f:
            plaintext = f.read()

        remainder = len(plaintext) % 16
        padding = b' ' * (16 - remainder)
        plaintext += padding

        cipher = AES.new(key, AES.MODE_CBC, iv)

        ciphertext = cipher.encrypt(plaintext)

        output_file_path = os.path.join(os.path.dirname(file_path),
                                        'ec_' + os.path.basename(file_path))

        with open(output_file_path, 'wb') as f:
            f.write(ciphertext)

    @staticmethod
    def aes_decrypt(file_path):
        key = b'0123456789abcdef'
        iv = b'fedcba9876543210'

        with open(file_path, 'rb') as f:
            ciphertext = f.read()

        cipher = AES.new(key, AES.MODE_CBC, iv)

        plaintext = cipher.decrypt(ciphertext)

        output_file_path = os.path.join(os.path.dirname(file_path),
                                        'dc_' + os.path.basename(file_path)[3:])

        with open(output_file_path, 'wb') as f:
            f.write(plaintext.rstrip(b' '))
