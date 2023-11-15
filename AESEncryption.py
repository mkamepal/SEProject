from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import numpy as np
import constants as constants
class AESEncryption:

    global encrypt_cipher
    encrypt_cipher = AES.new(constants.AES_KEY, AES.MODE_CBC)
    AES_IV = encrypt_cipher.iv
    global decrypt_cipher
    decrypt_cipher = AES.new(constants.AES_KEY, AES.MODE_CBC, AES_IV)

    def aes_encrypt(coff_array):
       return encrypt_cipher.encrypt(pad(bytearray(coff_array.reshape(constants.RESHAPE)), AES.block_size, style='pkcs7'))

    def aes_decrypt(byte_array):
        return (np.frombuffer(unpad(decrypt_cipher.decrypt(byte_array), 16), np.float32)).reshape(constants.SHAPE)

