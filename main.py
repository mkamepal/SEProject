import matplotlib.pyplot as plt
import matplotlib.image as image
import time

import numpy as np
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from pywtconversion import *
from AESEncryption import *
from DES3Encryption import *
from RSAEncryption import *


import constants as constants

global encrypted_approximation, encrypted_horizontal, encrypted_vertical, encrypted_diagonal
global decrypted_approximation, decrypted_horizontal, decrypted_vertical, decrypted_diagonal

def encrypt_using_aes(encrypt_array):
    return AESEncryption.aes_encrypt(encrypt_array)

def decrypt_using_aes(decrypt_array):
    return AESEncryption.aes_decrypt(decrypt_array)

def encrypt_using_des(encrypt_array):
    return DES3Encryption.des_encrypt(encrypt_array)

def decrypt_using_des(decrypt_array):
    return DES3Encryption.des_decrypt(decrypt_array)

def encrypt_using_rsa(encrypt_array):
    return RSAEncryption.rsa_encrypt(encrypt_array)

def decrypt_using_rsa(decrypt_rsa):
    return RSAEncryption.rsa_decrypt(decrypt_rsa)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_image = image.imread(r"images/image1.png")
    Approximation, (Horizontal_Segment, Vertical_segment, Diagonal_segment) = pywtconversion.convert_to_pywtcoff(input_image)
    #print(Approximation)
    encrypted_approximation = encrypt_using_aes(Approximation)
    decrypted_approximation = decrypt_using_aes(encrypted_approximation)
    restord_image = pywtconversion.restore_orignal_image(decrypted_approximation, Horizontal_Segment, Vertical_segment, Diagonal_segment)
    print(constants.RESHAPE)
    print(constants.SHAPE)



