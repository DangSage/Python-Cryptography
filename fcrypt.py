from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from os import urandom

# Params

# Setup
data = b"Hello World!"
key = urandom(16)

print("Before Encryption / Decryption Process")
print(data)
sender_private_key = RSA.generate(2048)
sender_public_key = sender_private_key.public_key()

receiver_private_key = RSA.generate(2048)
receiver_public_key = receiver_private_key.public_key()

# Data Encryption
# use "key" to encript "data"
aes_encript_object = AES.new(key, AES.MODE_GCM)
ciphertext, tag = aes_encript_object.encrypt_and_digest(data)
nonce = aes_encript_object.nonce

# Key Encription
rsa_encrypt_object = PKCS1_OAEP.new(receiver_public_key)
key_ciphertext = rsa_encrypt_object.encrypt(key)

# Message Concatenation
concentrated_message = f"{ciphertext}\n|\n{tag}\n|\n{nonce}\n|\n{key_ciphertext}"
print("During Encryption / Decryption Process")
print(concentrated_message)

# Message De-Concatenation
# separated_message = concentrated_message.split("|")
# ciphertext = separated_message[0]
# tag = separated_message[1]
# nonce = separated_message[2]
# key_ciphertext = separated_message[3]

# Key Dencryption
rsa_decrypt_object = PKCS1_OAEP.new(receiver_private_key)
decrypted_key = rsa_decrypt_object.decrypt(key_ciphertext)

# Message Decryption
aes_decrypt_object = AES.new(decrypted_key, AES.MODE_GCM, nonce=aes_encript_object.nonce)
decrypted_message = aes_decrypt_object.decrypt_and_verify(ciphertext, tag)

print("After Encryption / Decryption Process")
print(decrypted_message)
