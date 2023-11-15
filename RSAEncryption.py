from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import numpy as np

import constants


class RSAEncryption:

    global key, private_key, public_key, chunk_size, RSA_encryptor, RSA_decryptor
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    chunk_size = 210

    RSA_encryptor = PKCS1_OAEP.new(RSA.import_key(public_key))

    RSA_decryptor = PKCS1_OAEP.new(RSA.import_key(private_key))

    def rsa_encrypt(coff_array):
        encrypted_chunks = []
        coff_array_reshaped = bytearray(coff_array.reshape(constants.RESHAPE))
        chunks = [coff_array_reshaped[c : c + chunk_size] for c in range(0, len(coff_array_reshaped), chunk_size)]
        for chunk in chunks:
            encrypted_chunk = RSA_encryptor.encrypt(chunk)
            encrypted_chunks.append(encrypted_chunk)
        return encrypted_chunks

    def rsa_decrypt(byte_array):
        decrypted_chunks = []
        for encrypted_chunk in byte_array:
            decrypted_chunk = RSA_decryptor.decrypt(encrypted_chunk)
            decrypted_chunks.append(decrypted_chunk)
        return np.frombuffer(b''.join(decrypted_chunks), dtype=np.float32).reshape(constants.SHAPE)




