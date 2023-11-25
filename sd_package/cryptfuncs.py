"""Module that contains functions for encrypting and decrypting passwords using RSA encryption. 
    It also contains a function for generating RSA key pairs.
    
    This is the only module that needs to be imported in order to use the encryption functions within the SecureDrop package."""

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Hash import SHA256

def generate_key_pair():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()

    private_pem = private_key.exportKey()
    public_pem = public_key.exportKey()

    return private_pem, public_pem

def encrypt_password(public_key, password):
    public_key = RSA.importKey(public_key)
    cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
    encrypted_password = cipher.encrypt(password.encode())

    return encrypted_password

def decrypt_password(private_key, encrypted_password):
    private_key = RSA.importKey(private_key)
    cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
    decrypted_password = cipher.decrypt(encrypted_password)

    return decrypted_password.decode()