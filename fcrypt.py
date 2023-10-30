"""This is our encryption file. It will be used to encrypt and decrypt files."""

import argparse
from os import urandom
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES

# this program uses PGP encryption to encrypt and decrypt files using a public key and private key

# To run this program, use the following command:
# python fcrypt.py --encrypt <input file> <output file>

# Parse arguments
parser = argparse.ArgumentParser(description='Encrypt or decrypt files using PGP scheme')
parser.add_argument('--encrypt', action='store_true', help='Encrypt file')
parser.add_argument('--decrypt', action='store_true', help='Decrypt file')
parser.add_argument('key', type=str, help='Public key for encryption or private key for decryption')
parser.add_argument('input_file', type=str, help='Input file path')
parser.add_argument('output_file', type=str, help='Output file path')
args = parser.parse_args()

# Setup
with open(args.input_file, 'rb') as f:
    DATA = f.read()

# Debugging purposes
print("Before Encryption / Decryption Process:\n====================")
print(DATA)

if args.encrypt:
    # Load recipient's public key from file
    receiver_public_key = RSA.import_key(open(args.key).read())

    # Generate key
    key = urandom(16)
    # Encrypt message
    aes_encrypt_object = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = aes_encrypt_object.encrypt_and_digest(DATA)

    # Encrypt key
    rsa_encrypt_object = PKCS1_OAEP.new(receiver_public_key)
    key_ciphertext = rsa_encrypt_object.encrypt(key)
    # Concentrate message
    ENCRYPTED = b'\n|\n'.join([ciphertext, tag, aes_encrypt_object.nonce, key_ciphertext])

    # Write encrypted message to output file
    with open(args.output_file, 'wb') as f:
        f.write(ENCRYPTED)
    print(f"\n> Encryption Successful: message written to {args.output_file}")

elif args.decrypt:
    # Load recipient's private key from file
    receiver_private_key = RSA.import_key(open(args.key).read())

    # Split message
    ciphertext, tag, nonce, key_ciphertext = DATA.split(b'\n|\n')

    # Decrypt key
    rsa_decrypt_object = PKCS1_OAEP.new(receiver_private_key)
    key = rsa_decrypt_object.decrypt(key_ciphertext)
    
    # Decrypt message
    aes_decrypt_object = AES.new(key, AES.MODE_GCM, nonce)
    plaintext = aes_decrypt_object.decrypt_and_verify(ciphertext, tag)

    # Write decrypted message to output file
    with open(args.output_file, 'wb') as f:
        f.write(plaintext)
    print(f"\n> Decryption Successful: message written to {args.output_file}")
