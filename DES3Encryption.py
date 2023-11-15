from Crypto.Cipher import DES3

import constants as constants
import numpy as np

class DES3Encryption:

    global encryption_cipher
    encryption_cipher = DES3.new(constants.DES_KEY, DES3.MODE_CBC)

    DES_IV = encryption_cipher.IV

    global decryption_cipher
    decryption_cipher = DES3.new(constants.DES_KEY, DES3.MODE_CBC, DES_IV)


    def des_encrypt(waveCoff):
        return encryption_cipher.encrypt(bytearray(waveCoff.reshape(constants.RESHAPE)))

    def des_decrypt(byte_array):
        return np.frombuffer(decryption_cipher.decrypt(byte_array), np.float32).reshape((constants.SHAPE))