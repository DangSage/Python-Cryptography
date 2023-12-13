@echo off
setlocal

:: Create the client certificate directory in the current directory
mkdir bin\certs\client_%1

:: Generate a new private key
openssl genpkey -algorithm RSA -out key.pem

:: Generate a CSR using the private key
openssl req -new -key key.pem -out request.csr -subj "/CN=localhost/O=client/OU=%1"

:: Sign the CSR using the CA, creating a new certificate
openssl x509 -req -in request.csr -CA bin/ca.crt -CAkey bin/ca.key -out cert.crt

:: Remove the CSR
del request.csr

:: Move the files to the correct location
move key.pem .\bin\certs\client_%1\%1key.pem
move cert.crt .\bin\certs\client_%1\%1cert.crt

endlocal