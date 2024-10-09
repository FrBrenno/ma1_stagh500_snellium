# libraries: licence

The daemon integrates a licence feature to prevent unauthorized use of it.
The licencing system rely on certificates files, the protected features are
unlocked when the user provides a valid certificate.

## Certificates

Inside certificates, multiple elements protects different cases of malicious
usage:

- Computer fingerprint, created from the hardware-queries module, used to
  ensure that the certificate has been created for the current machine.
- Expiration date, used to limit in time the validity of the certificate.
- Cryptographic signature, used to check that the certificate has not been 
  falsified by an unauthorized organisation or person.

A certificate is considered valid only if all verifications are together 
successful.

## Architecture 

The main class of the module is the `CertificateManager` class, 
that load certificates and verify their authenticity using the `Verifier` class.

## Signature

The signature uses an asymmetric encryption scheme. The public key is 
distributed with the software while the private key is kept private by 
Snellium. Signature can only be forged with knowledge of both keys, but can
be verified using the public key only.

The public key is embedded inside the binaries when the application is
distributed, to ensure that it is not modified.
