from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import base64


private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)


pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)


with open("extension_private.pem", "wb") as f:
    f.write(pem)


public_key = private_key.public_key()


der = public_key.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)


key = base64.b64encode(der).decode()


print("\nADD THIS TO manifest.json:\n")
print('"key": "' + key + '"')