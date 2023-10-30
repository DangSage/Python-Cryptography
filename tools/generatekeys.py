"""This is a debug tool to generate key pairs for testing purposes."""
import argparse
import os
import sys
import time
from Crypto.PublicKey import RSA

# Parse command line arguments
parser = argparse.ArgumentParser(description="Generate key pairs for testing purposes.")
parser.add_argument("directory", type=str, help="Directory to store key pairs")
parser.add_argument("--keyname", type=str, help="Name of the key pair")
parser.add_argument("--keysize", type=int, default=2048, help="Size of the RSA key in bits")
args = parser.parse_args()

# Generate a unique key pair and store it in the directory defined as an argument
def generate_key_pair(directory, keyname, keysize):
    prefix = f"{keyname}_" if keyname else ""
    private_key = RSA.generate(keysize)
    public_key = private_key.publickey()
    with open(os.path.join(directory, f"{prefix}private.pem"), "wb") as private_key_file:
        private_key_file.write(private_key.exportKey('PEM'))
    with open(os.path.join(directory, f"{prefix}public.pem"), "wb") as public_key_file:
        public_key_file.write(public_key.exportKey('PEM'))
    print(f"Key pair generated and stored in: {directory}")

# Confirm that the user wants to generate the key pair
confirmation = input("Are you sure you want to generate a new RSA key pair? (y/n): ")
if confirmation.lower() != "y":
    print("Exiting...")
    sys.exit()

# Check that the directory exists and is writable
if not os.path.isdir(args.directory):
    print("Error: Directory does not exist.")
    sys.exit()
if not os.access(args.directory, os.W_OK):
    print("Error: Directory is not writable.")
    sys.exit()

# Generate key pair
print("Generating RSA key pair...")
start_time = time.time()
generate_key_pair(args.directory, args.keyname, args.keysize)
end_time = time.time()
print(f"RSA key pair generated in {end_time - start_time:.2f} seconds.")