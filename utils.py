import numpy as np
from heaan_utils import HEAAN

he = HEAAN()
he.initialize()


def max_pooling(image_array, pool_size, stride):
    matrix_data = image_array / 255 - 0.5

    encrypted_lists = he.send_data(matrix_data=matrix_data, n=pool_size, s=stride)

    sorted_lists = he.sort_encrypt_messages(encrypted_lists)

    result = he.receive_data(sorted_lists)

    return (result + 0.5) * 255


def approx_max_pooling(image_array, pool_size, stride):
    matrix_data = image_array/255 - 0.5

    encrypted_lists = he.send_data_approx(matrix_data=matrix_data, n=pool_size, s=stride)

    sorted_lists = he.max_encrypt_messages(encrypted_lists)

    result = he.receive_data(sorted_lists)
    return abs((result + 0.5) * 255 * 2)