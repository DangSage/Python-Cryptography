"""This is our encryption file. It will be used to encrypt and decrypt files."""

import argparse
from os import urandom
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES

# Currently this iteration of the program only supports encryption
# This commit only takes encrypt and plaintext as an argument and will not run if decrypt is specified
# The program will generate a public and private key for the sender and receiver and output
# the encrypted message to the output file specified by the user
# The program will also output the private key of the sender for debugging purposes

# To run this program, use the following command:
# python fcrypt.py --encrypt <input file> <output file>

# Parse arguments
parser = argparse.ArgumentParser(description='Encrypt or decrypt files using PGP scheme')
parser.add_argument('--encrypt', action='store_true', help='Encrypt file')
parser.add_argument('--decrypt', action='store_true', help='Decrypt file')
#parser.add_argument('key', type=str, help='Public key for encryption or private key for decryption')
parser.add_argument('input_file', type=str, help='Input file path')
parser.add_argument('output_file', type=str, help='Output file path')
args = parser.parse_args()

# Setup
with open(args.input_file, 'rb') as f:
    DATA = f.read()

key = urandom(16)

print("Before Encryption / Decryption Process:\n====================")
print(DATA)

if args.encrypt:
    sender_private_key = RSA.generate(2048)
    sender_public_key = sender_private_key.public_key()

    receiver_private_key = RSA.generate(2048)
    receiver_public_key = receiver_private_key.public_key()

    # Data Encryption
    # use "key" to encrypt "DATA"
    aes_encript_object = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = aes_encript_object.encrypt_and_digest(DATA)
    nonce = aes_encript_object.nonce

    # Key Encryption
    rsa_encrypt_object = PKCS1_OAEP.new(receiver_public_key)
    key_ciphertext = rsa_encrypt_object.encrypt(key)

    # Write the keys to output for debugging purposes
    with open("sender_private_key.pem", 'wb') as f:
        f.write(sender_private_key.export_key('PEM'))
        
    # Message Concatenation
    concentrated_message = f"{ciphertext}\n|\n{tag}\n|\n{nonce}\n|\n{key_ciphertext}"
    print("\nDuring Encryption / Decryption Process:\n===================="+concentrated_message)    # Debugging purposes

    # Write encrypted message to output file
    with open(args.output_file, 'wb') as f:
        f.write(concentrated_message.encode())
    print(f"\n> Encryption Successful: message written to {args.output_file}")

# Message De-Concatenation
# elif args.decrypt:
    # separated_message = concentrated_message.split("|")
    # ciphertext = separated_message[0]
    # tag = separated_message[1]
    # nonce = separated_message[2]
    # key_ciphertext = separated_message[3]

    # Key Dencryption
    # rsa_decrypt_object = PKCS1_OAEP.new(receiver_private_key)
    # decrypted_key = rsa_decrypt_object.decrypt(key_ciphertext)

    # Message Decryption
    # aes_decrypt_object = AES.new(decrypted_key, AES.MODE_GCM, nonce=aes_encript_object.nonce)
    # decrypted_message = aes_decrypt_object.decrypt_and_verify(ciphertext, tag)

    # print("After Encryption / Decryption Process")
    # print(decrypted_message)
