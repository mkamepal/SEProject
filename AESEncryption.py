from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import numpy as np
import constants as constants
class AESEncryption:

    global encryption_cipher
    encryption_cipher = AES.new(constants.AES_key, AES.MODE_CBC)
    AES_IV = encryption_cipher.iv
    global decrypt_cipher
    decrypt_cipher = AES.new(constants.AES_key, AES.MODE_CBC, AES_IV)

    def aes_encryption(coff_array):
       return encryption_cipher.encrypt(pad(bytearray(coff_array), AES.block_size, style='pkcs7'))

    def aes_decryptor(byte_array):
        return np.frombuffer(unpad(decrypt_cipher.decrypt(byte_array), 16))