import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from cryptography.fernet import Fernet


def encrypt(key, filename):
    chunksize = 64 * 1024
    outputFile = "ec_" + filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)

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


def decrypt(key, filename):
    chunksize = 64 * 1024
    outputFile = filename[3:]

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(filesize)


def get_key(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()


def generate_key():
    return Random.new().read(32)


def encrypt_file(key, filepath):
    with open(filepath, 'rb') as infile:
        data = infile.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    output_folder = "ec_" + os.path.dirname(filepath)
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, os.path.basename(filepath))

    with open(output_file, 'wb') as outfile:
        outfile.write(encrypted)


def decrypt_file(key, filepath):
    with open(filepath, 'rb') as infile:
        data = infile.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    output_folder = "dc_" + os.path.dirname(filepath)[3:]
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, os.path.basename(filepath)[3:])

    with open(output_file, 'wb') as outfile:
        outfile.write(decrypted)


def encrypt_folder(folder_path):
    key = Fernet.generate_key()

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            encrypt_file(key, filepath)

    return key


def decrypt_folder(key, foldername):
    for root, dirs, files in os.walk(foldername):
        for file in files:
            filepath = os.path.join(root, file)
            decrypt(key, filepath)
            os.remove(filepath)
            os.rename(os.path.join(root, "dc_" + file), os.path.join(root, file))
