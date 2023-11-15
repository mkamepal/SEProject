import pywt
import constants as constants
import numpy as np
class pywtconversion:

    def convert_to_pywtcoff(image):
        wavelet_coeffs = pywt.dwt2(image, 'haar')
        Approximation, (Horizontal_Segment, Vertical_segment, Diagonal_segment) = wavelet_coeffs
        constants.SHAPE = Approximation.shape
        constants.RESHAPE = np.prod(Approximation.shape)
        return Approximation, (Horizontal_Segment, Vertical_segment, Diagonal_segment)

    def restore_orignal_image(Approximation, Horizontal_Segment, Vertical_segment, Diagonal_segment):
        image = pywt.waverec2(Approximation, (Horizontal_Segment, Vertical_segment, Diagonal_segment), 'haar')
        return image