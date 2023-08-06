from pycryptoguard import AESEncryption


def encrypt_file(input_file, output_file, key):
    encryption = AESEncryption(key)
    encryption.encrypt_file(input_file, output_file)


def decrypt_file(input_file, output_file, key):
    encryption = AESEncryption(key)
    encryption.decrypt_file(input_file, output_file)
