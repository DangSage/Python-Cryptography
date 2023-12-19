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
- Detects `users.json` and performs a first-time register function (one user per client).
- Salts and hashes passwords using SHA256 for secure storage in `users.json`.
- Generates a different key/certificate pair for communication on every login.

**Broadcast UDP**
- Listens on a specific port with `broadcast_listen` thread.
- Sends a ping with the client's data to ports 1337-2000 with `broadcast_send` thread.
- Builds a database of online clients (not contacts).

**TCP Connection with SSL/TLS**
- Transfers real data via a TCP connection with an SSL/TLS scheme.
- Makes the TCP connection by wrapping a TLS socket with the user's key (generated on startup) and certificate (generated with the CA in the project directory).
- Includes a copy of the public certificate being exchanged in every request made over the TCP connection to verify data being sent.

**File Transfer**
- Sends files over the TLS handshake connection using symmetric encryption.
- Generates an AES symmetric key, encrypts the file with this key, and then encrypts the key with the recipient's public key.
- Encodes the encrypted file info into a base64 encoded tuple and sends it to the recipient.
- Decrypts the AES symmetric key with their own RSA private key, decrypts the file from the base64 decoded encrypted file info, and writes it to the file name in the project directories /downloads folder.

**Control Flow Management**
- Implements a message limit and a counter to track the number of processed messages, along with a timestamp marking the start of the counter.
- Increments the counter with each processed message. Upon reaching the limit, measures the time elapsed since the start.
- Pauses for the remaining duration if less than a second has passed, effectively capping the message processing rate to the set limit per second.
- Provides safeguard against flooding DoS attacks by restricting the volume of requests that can be made.

**Timestamps**
- Embeds a timestamp iso object into every File transfer request.
- Provides protection against replay attacks.

**Session Token**
- Generates a unique random string of characters as UID for each login session.
- Associates the session token with the user's email for every online user they ping, it remains unchanged until the users session quits and goes offline.
- Ensures that there can be only one session per device on a network, and also ensures that any device on the local network cannot impersonate the client's user when online.