import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac

def encrypt_data():
    secret_string = os.environ.get('HASH_SECRET')
    print("Secret key: ", secret_string)
    pin_hash = hmac.HMAC(secret_string, hashes.SHA224(), backend=default_backend)
    pin_hash.update("4040")
    pin_hash.finalize()
##problemas con el envtest.py file, dice que no soporta el algoritmo pero, idk,
# encrypt_data()