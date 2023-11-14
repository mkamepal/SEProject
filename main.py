import matplotlib.pyplot as plt
import matplotlib.image as image
import PIL.Image as Image
import imageio
import cv2
import pywt
import numpy as np
import time
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.py3compat import *
from Crypto.Cipher import PKCS1_OAEP



def encryptImage(image):
    wavelet_coeffs = pywt.dwt2(image, 'haar')
    Approximation, (Horizontal_Segment, Vertical_segment, Diagonal_segment) = wavelet_coeffs
    shape = Approximation.shape

    size = np.prod(shape)
    Approximation = Approximation.reshape(size)
    Approximation_b = bytearray(Approximation)
    Horizontal_Segment = Horizontal_Segment.reshape(size)
    Horizontal_Segment_b = bytearray(Horizontal_Segment)
    Vertical_segment = Vertical_segment.reshape(size)
    Vertical_segment_b = bytearray(Vertical_segment)
    Diagonal_segment = Diagonal_segment.reshape(size)
    Diagonal_segment_b = bytearray(Diagonal_segment)
    cipher = AES.new(AES_key, AES.MODE_CBC)
    AES_IV = cipher.iv
    Approximation_encrypted = cipher.encrypt(pad(Approximation_b, AES.block_size, style='pkcs7'))
    Horizontal_Segment_encrypted = cipher.encrypt(pad(Horizontal_Segment_b, AES.block_size, style='pkcs7'))
    Vertical_segment_encrypted = cipher.encrypt(pad(Vertical_segment_b, AES.block_size, style='pkcs7'))
    Diagonal_segment_encrypted = cipher.encrypt(pad(Diagonal_segment_b, AES.block_size, style='pkcs7'))
    return Approximation_encrypted, Horizontal_Segment_encrypted, Vertical_segment_encrypted, Diagonal_segment_encrypted, AES_IV, shape
def decryptImage(approximation, horizontal, vertical, diagonal, AES_IV, shape):
    cipher2 = AES.new(AES_key, AES.MODE_CBC, AES_IV)
    Approximation_dencrypted = unpad(cipher2.decrypt(approximation), 16)
    Horizontal_Segment_dencrypted = unpad(cipher2.decrypt(horizontal), 16)
    Vertical_segment_dencrypted = unpad(cipher2.decrypt(vertical), 16)
    Diagonal_segment_dencrypted = unpad(cipher2.decrypt(diagonal), 16)
    Approximation_restored = (np.frombuffer(Approximation_dencrypted, dtype=np.float32)).reshape(shape)
    Horizontal_Segment_restored = (np.frombuffer(Horizontal_Segment_dencrypted, dtype=np.float32)).reshape(shape)
    Vertical_segment_restored = (np.frombuffer(Vertical_segment_dencrypted, dtype=np.float32)).reshape(shape)
    Diagonal_segment_restored = (np.frombuffer(Diagonal_segment_dencrypted, dtype=np.float32)).reshape(shape)
    wavelet_coeff_restored = Approximation_restored, (Horizontal_Segment_restored, Vertical_segment_restored, Diagonal_segment_restored)
    image = pywt.waverec2(wavelet_coeff_restored, 'haar')

def runAES(image):
    approximation, horizontal, vertical, diagonal, iv, shape = encryptImage(image)
    decryptImage(approximation, horizontal, vertical, diagonal, iv, shape)

def runRSA(image):
    wavelet_coeffs = pywt.dwt2(image, 'haar')
    Approximation, (Horizontal_Segment, Vertical_segment, Diagonal_segment) = wavelet_coeffs
    shape = Approximation.shape

    size = np.prod(shape)

    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    chunk_size = 210
    layers = [Approximation, Horizontal_Segment, Vertical_segment, Diagonal_segment]
    starttime = time.time()
    encrypted_chunks = [[],[],[],[]]
    for z in range(1):
        layers[z] = bytearray(layers[z].reshape(size))
        chunks = [layers[z][i:i + chunk_size] for i in range(0, len(layers[z]), chunk_size)]
        cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
        for chunk in chunks:
            encrypted_chunk = cipher.encrypt(chunk)
            encrypted_chunks[z].append(encrypted_chunk)
    endtime = time.time()
    print(endtime-starttime)
    encrypted_array = [[],[],[],[]]
    for z in range(1):
        encrypted_array = layers
        encrypted_array[z] = b''.join(encrypted_chunks[z])
        encrypted_array[z] = encrypted_array[z][:size*4]
        encrypted_array[z] = (np.frombuffer(encrypted_array[z], dtype=np.float32)).reshape(shape)
    wavelet_coeff_restored = encrypted_array[0], (encrypted_array[1], encrypted_array[2], encrypted_array[3])
    image = pywt.waverec2(wavelet_coeff_restored, 'haar')
    plt.imshow(image)
    plt.show()
    starttime = time.time()

    for z in range(1):
        decrypted_chunks = []
        cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
        for encrypted_chunk in encrypted_chunks[z]:
            decrypted_chunk = cipher.decrypt(encrypted_chunk)
            decrypted_chunks.append(decrypted_chunk)

        layers[z] = b''.join(decrypted_chunks)
        layers[z] = (np.frombuffer(layers[z], dtype=np.float32)).reshape(shape)
    wavelet_coeff_restored = layers[0], (layers[1], layers[2], layers[3])

    image = pywt.waverec2(wavelet_coeff_restored, 'haar')
    endtime = time.time()
    print(endtime - starttime)
    plt.imshow(image)
    plt.show()
def runBenchmark(image):
    starttime = time.time()
    runAES(image)
    endtime = time.time()
    print("Time to encrypt & decrypt with AES: "+str(endtime-starttime))
    starttime = time.time()
    runRSA(image)
    endtime = time.time()
    print("Time to encrypt & decrypt with RSA: "+str(endtime-starttime))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_image = image.imread(r"images/img.png")
    print(input_image)
    global AES_key
    AES_key = b'Agri crypto key1'
    runBenchmark(input_image)



