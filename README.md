# Secure Airdrop with Cryptography

This project aims to create a secure cryptographic version of an airdrop mechanism using Python. We employ both symmetric and asymmetric cryptography, specifically RSA and AES, to achieve our goal.

For external users, it's important to know the fundamental concepts of symmetric and asymmetric cryptography, as this project showcases their practical application in securing data transfers. Knowledge of Python and the PyCryptodome library will be helpful for understanding the implementation details.

Must have the pycryptodomex library installed to run using pip:
- `pip install pycryptodomex`

SecureDrop also runs as a shell within the driver module `secure_drop.py`. Run this driver module to start up the application.


## Milestones
The project is divided into milestones for each feature of the project. Current milestones are listed as below, with their features:

**Milestone 1 - User Registration**
  - Use simple file structures for data storage.
  - Implement security measures after initial testing.
  - Reuse password protections in User Login milestone.
  - Use Python crypt module for password security.
  - Generate and store data for future mutual using RSA encryption with SHA256 hashing.

**Milestone 2 - User Login**
  - Reuse code from User Registration milestone.
  - Use login data to enhance security in future milestones.
  - Clear all data from memory on program exit.

**Milestone 3 - Adding Contacts**
  - Use simple file structures for data storage.
  - Use Milestone 2 data to secure contact information.

**Milestone 4 - Detecting Contacts**
  - Use UDP connection to broadcast logins from other clients

**Milestone 5 - File Transfer**
  - Files are sent over TCP SSL/TLS handshake connection using symmetric encryption.
  - The recipient decrypts the AES symmetric key with their own RSA private key, decrypts the file and writes it to download


## Features

**User Registration and Login**
- The login shell detects for `users.json` and performs a first-time register function (there should only be 1 user per client).
- Passwords are salted and hashed using SHA256 for secure storage in `users.json`.
- Every login generates a different key/certificate pair for communication.

**Broadcast UDP**
- The `broadcast_listen` thread listens on a specific port.
- The `broadcast_send` thread sends a ping with the client's data to ports 1337-2000.
- These threads build a database of online clients (not contacts).

**TCP Connection with SSL/TLS**
- Real data is transferred via a TCP connection with an SSL/TLS scheme.
- The TCP connection is made by wrapping a TLS socket with the user's key (generated on startup) and certificate (generated with the CA in the project directory).
- To verify data being sent, every request made over the TCP connection includes a copy of the public certificate being exchanged.

**File Transfer**
- Files are sent over the TLS handshake connection using symmetric encryption.
- The system generates an AES symmetric key, encrypts the file with this key, and then encrypts the key with the recipient's public key.
- The encrypted file info is encoded into a base64 encoded tuple and sent to the recipient.
- The recipient decrypts the AES symmetric key with their own RSA private key, decrypts the file from the base64 decoded encrypted file info, and writes it to the file name in the project directories /downloads folder.
