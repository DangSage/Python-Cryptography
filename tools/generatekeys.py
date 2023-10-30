"""This is a debug tool to generate key pairs for testing purposes."""
import argparse
from Crypto.PublicKey import RSA

# Parse command line arguments
parser = argparse.ArgumentParser(description="Generate key pairs for testing purposes.")
parser.add_argument("directory", type=str, help="Directory to store key pairs")
args = parser.parse_args()

# Generate a unique key pair and store it in the directory defined as an argument
def generate_key_pair(directory):
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    private_key_file = open(directory + "/private.pem", "wb")
    private_key_file.write(private_key.exportKey('PEM'))
    private_key_file.close()
    public_key_file = open(directory + "/public.pem", "wb")
    public_key_file.write(public_key.exportKey('PEM'))
    public_key_file.close()
    print("Key pair generated and stored in " + directory + ".")

# Generate key pair
generate_key_pair(args.directory)

