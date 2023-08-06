import os
from Crypto.Cipher import AES

class PyEncrypt:
    @staticmethod
    def aes_encrypt_file(file_path, key=b'0123456789abcdef', iv=b'fedcba9876543210'):
        with open(file_path, 'rb') as f:
            plaintext = f.read()

        remainder = len(plaintext) % 16
        padding = b' ' * (16 - remainder)
        plaintext += padding

        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(plaintext)

        output_file_path = os.path.join(os.path.dirname(file_path), 'ec_' + os.path.basename(file_path))

        with open(output_file_path, 'wb') as f:
            f.write(ciphertext)

    @staticmethod
    def aes_encrypt_folder(folder_path, key=b'0123456789abcdef', iv=b'fedcba9876543210'):
        output_folder_path = os.path.join(os.path.dirname(folder_path), 'ec_' + os.path.basename(folder_path))
        os.makedirs(output_folder_path, exist_ok=True)

        for root, _, files in os.walk(folder_path):
            for file in files:
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(output_folder_path, 'ec_' + file)
                PyEncrypt.aes_encrypt_file(input_file_path, key, iv)
                os.replace(os.path.join(os.getcwd(), 'ec_' + input_file_path), output_file_path)

    @staticmethod
    def aes_decrypt_file(file_path, key=b'0123456789abcdef', iv=b'fedcba9876543210'):
        with open(file_path, 'rb') as f:
            ciphertext = f.read()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)

        output_file_path = os.path.join(os.path.dirname(file_path), 'dc_' + os.path.basename(file_path))

        with open(output_file_path, 'wb') as f:
            f.write(plaintext.rstrip())

    @staticmethod
    def aes_decrypt_folder(folder_path, key=b'0123456789abcdef', iv=b'fedcba9876543210'):
        output_folder_path = os.path.join(os.path.dirname(folder_path), 'dc_' + os.path.basename(folder_path))
        os.makedirs(output_folder_path, exist_ok=True)

        for root, _, files in os.walk(folder_path):
            for file in files:
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(output_folder_path, 'dc_' + file)
                PyEncrypt.aes_decrypt_file(input_file_path, key, iv)
                os.replace(os.path.join(os.getcwd(), 'dc_' + input_file_path), output_file_path)
