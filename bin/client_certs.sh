# Create the client cert directory in the current directory
mkdir -p ./bin/certs/client

# Generate a new private key
openssl genpkey -algorithm RSA -out key.pem

# Generate a CSR using the private key
openssl req -new -key key.pem -out request.csr -subj "/CN=localhost/O=client/OU=$1"

# Sign the CSR using the CA, creating a new certificate
openssl x509 -req -in request.csr -CA ca.crt -CAkey ca.key -out cert.crt

chmod 400 key.pem

# Remove the CSR
rm request.csr

# Move the files to the correct location
mv key.pem ./bin/certs/client/key.pem
mv cert.crt ./bin/certs/client/cert.crt

