import matplotlib.pyplot as plt
import matplotlib.image as image
from PIL import Image
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
def apply_selective_encryption(input_image):
    Approximation, (Horizontal_Segment, Vertical_segment, Diagonal_segment) = pywtconversion.convert_to_pywtcoff(input_image)
    encrypted_approximation = encrypt_using_aes(Approximation)
    encrypted_horizontal = encrypt_using_des(Horizontal_Segment)
    encrypted_data = encrypted_approximation, (encrypted_horizontal, Vertical_segment, Diagonal_segment)
    return encrypted_data

def construct_encrypted_image(encrypted_data):
    Approximation, (Horizontal_Segment, Vertical_segment, Diagonal_segment) = encrypted_data
    encrypted_approximation = (np.frombuffer(Approximation[:-16], dtype=np.float32)).reshape((constants.SHAPE))
    encrypted_horizontal = (np.frombuffer(Horizontal_Segment, dtype=np.float32)).reshape((constants.SHAPE))
    image = pywtconversion.restore_orignal_image(encrypted_approximation, encrypted_horizontal, Vertical_segment, Diagonal_segment)
    return image

def apply_decryption(encrypted_data):
    Approximation, (Horizontal_Segment, Vertical_segment, Diagonal_segment) = encrypted_data
    decrypted_approximation = decrypt_using_aes(Approximation)
    decrypted_horizontal = decrypt_using_des(Horizontal_Segment)
    image = pywtconversion.restore_orignal_image(decrypted_approximation, decrypted_horizontal, Vertical_segment, Diagonal_segment)
    return image


if __name__ == '__main__':
    input_image = image.imread(r"images/image1.png")
    print(np.min(input_image), np.max(input_image))
    encrypted_data = apply_selective_encryption(input_image)
    encrypted_image = construct_encrypted_image(encrypted_data)
    decrypted_image = apply_decryption(encrypted_data)
    plt.imsave("/home/mahesh/Desktop/AGRI_PROJECT/images/encrypted.png", (encrypted_image * 255).astype(np.uint8))
    plt.imsave("/home/mahesh/Desktop/AGRI_PROJECT/images/depcryptedimage.png", (decrypted_image * 255).astype(np.uint8))



