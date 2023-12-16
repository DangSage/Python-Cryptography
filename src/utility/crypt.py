import os
import base64
import json
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
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

def pub_from_pem(pem_cert):
    '''
    return the public key from a PEM certificate
    '''
    cert = RSA.importKey(pem_cert.decode())
    return cert.publickey().exportKey().decode()

def generate_key_pair():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()

    private_pem = private_key.exportKey()
    public_pem = public_key.exportKey()

    return private_pem, public_pem


def encrypt_file(file_name, public_key):
    '''
    encrypt a file with RSA using the public key of the recipient
    
    Encryption Process:
    open file -> encrypt file (RSA) -> encode (base64) -> concatenate with filename -> convert to JSON
    '''
    recipient_key = RSA.importKey(public_key)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)

    with open(file_name, 'rb') as f:
        file_data = f.read()

    encrypted_data = cipher_rsa.encrypt(file_data)
    message = json.dumps({
        'filename': os.path.basename(file_name),
        'filedata': base64.b64encode(encrypted_data).decode('utf-8')
    })
    return message


def decrypt_file(file_data):
    '''
    decrypt a file with RSA using the private key of the recipient (current user)
    
    Decryption Process:
    decode (base64) -> decrypt file (RSA) -> open file
    '''
    recipient_key = RSA.importKey(ng.KEY)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)

    file_data = json.loads(file_data)
    encrypted_data = base64.b64decode(file_data['filedata'])

    decrypted_data = cipher_rsa.decrypt(encrypted_data)
    file_path = os.path.join(gl.DOWNLOAD_DIR, file_data['filename'])
    try:
        with open(file_path, 'wb') as f:
            f.write(decrypted_data)
            f.close()
    except IOError as e:
        print(f"File error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
