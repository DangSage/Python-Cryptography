openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 365 -key ca.key -out ca.crt -subj "/C=US/ST=MA/L=Lowell/O=SecureDrop/CN=localhost"