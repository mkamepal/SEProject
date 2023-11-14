import pywt

class pywt_conversion:

    def convert_to_pywtcoff(image):
        wavelet_coeffs = pywt.dwt2(image, 'haar')
        Approximation, (Horizontal_Segment, Vertical_segment, Diagonal_segment) = wavelet_coeffs
        return Approximation, (Horizontal_Segment, Vertical_segment, Diagonal_segment)

    def restore_orignal_image(Approximation, Horizontal_Segment, Vertical_segment, Diagonal_segment):
        image = pywt.waverec2(Approximation, (Horizontal_Segment, Vertical_segment, Diagonal_segment), 'haar')
        return image