import os
import base64
import json
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import PKCS1_OAEP, AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA256
import globals as gl
import nglobals as ng


def hash_password(password):
    salt = os.urandom(16)
    password_hash = PBKDF2(password, salt, 64, count=100000, hmac_hash_module=SHA256)
    return salt, password_hash


def check_password(salt, password_hash, password):
    new_hash = PBKDF2(password, salt, 64, count=100000, hmac_hash_module=SHA256)
    return new_hash == password_hash


def pub_from_pem(pem):
    return RSA.import_key(pem)


def generate_key_pair():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()

    private_pem = private_key.exportKey()
    public_pem = public_key.exportKey()

    return private_pem, public_pem


def encrypt_file(file_path, public_key):
    # Step 1: Encrypt the file
    symmetric_key = get_random_bytes(16)
    cipher_aes = AES.new(symmetric_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(open(file_path, 'rb').read())

    # Step 2: Encrypt the symmetric key
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(symmetric_key)

    # Step 3: Send the encrypted file and metadata
    encrypted_file_info = {
        'encrypted_key': base64.b64encode(encrypted_key).decode(),
        'nonce': base64.b64encode(cipher_aes.nonce).decode(),
        'tag': base64.b64encode(tag).decode(),
        'ciphertext': base64.b64encode(ciphertext).decode(),
    }

    return encrypted_file_info


def decrypt_file(encrypted_file_info):
    # Step 1: Decrypt the symmetric key
    private_key = RSA.import_key(open(ng.KEY, 'rb').read())
    cipher_rsa = PKCS1_OAEP.new(private_key)
    symmetric_key = cipher_rsa.decrypt(base64.b64decode(encrypted_file_info['encrypted_key']))

    # Step 2: Decrypt the file
    cipher_aes = AES.new(symmetric_key, AES.MODE_EAX, base64.b64decode(encrypted_file_info['nonce']))
    data = cipher_aes.decrypt_and_verify(base64.b64decode(encrypted_file_info['ciphertext']),
                                         base64.b64decode(encrypted_file_info['tag']))

    return data
