import os
from . import AESEncryption


def encrypt_file(input_file, output_file, password):
    encryption = AESEncryption(password)
    encryption.encrypt_file(input_file, output_file)


def decrypt_file(input_file, output_file, password):
    encryption = AESEncryption(password)
    encryption.decrypt_file(input_file, output_file)


def encrypt_folder(input_folder, output_folder, password):
    encryption = AESEncryption(password)
    os.makedirs(output_folder, exist_ok=True)
    for dirpath, dirnames, filenames in os.walk(input_folder):
        for file in filenames:
            input_path = os.path.join(dirpath, file)
            output_path = os.path.join(output_folder, file)
            encryption.encrypt_file(input_path, output_path)


def decrypt_folder(input_folder, output_folder, password):
    encryption = AESEncryption(password)
    os.makedirs(output_folder, exist_ok=True)
    for dirpath, dirnames, filenames in os.walk(input_folder):
        for file in filenames:
            input_path = os.path.join(dirpath, file)
            output_path = os.path.join(output_folder, file)
            encryption.decrypt_file(input_path, output_path)
