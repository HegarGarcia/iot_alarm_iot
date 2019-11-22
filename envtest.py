import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac

def patch_crypto_be_discovery():
    
    """
    Monkey patches cryptography's backend detection.
    Objective: support pyinstaller freezing.
    """

    from cryptography.hazmat import backends

    try:
        from cryptography.hazmat.backends.commoncrypto.backend import backend as be_cc
    except ImportError:
        be_cc = None

    try:
        from cryptography.hazmat.backends.openssl.backend import backend as be_ossl
    except ImportError:
        be_ossl = None

    backends._available_backends_list = [
        be for be in (be_cc, be_ossl) if be is not None
    ]
    print backends._available_backends_list

def encrypt_data():
    secret_string = os.environ.get('HASH_SECRET')
    print("Secret key: ", secret_string)
    pin_hash = hmac.HMAC(secret_string, hashes.SHA224(), backend=default_backend)
    pin_hash.update("4040")
    pin_hash.finalize()
##problemas con el envtest.py file, dice que no soporta el algoritmo pero, idk,