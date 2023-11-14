from Crypto.Cipher import DES3

import constants as constants
import numpy as np

class DES3Encryption:

    global encryption_cipher
    encryption_cipher = DES3.new(constants.DES_KEY, DES3.MODE_CBC)

    DES_IV = encryption_cipher.IV

    global decryption_cipher
    decryption_cipher = DES3.new(constants.DES_KEY, DES3.MODE_CBC, DES_IV)


    def des_encryptor(waveCoff):
        return encryption_cipher.encrypt(bytearray(waveCoff))

    def des_decryptor(byte_array):
        return np.frombuffer(decryption_cipher.decrypt(byte_array))