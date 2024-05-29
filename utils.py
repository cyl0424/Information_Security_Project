import numpy as np
from heaan_utils import HEAAN

he = HEAAN()
he.initialize()


def max_pooling(image_array, pool_size, stride):
    # h, w = image_array.shape
    # new_h = (h - pool_size) // stride + 1
    # new_w = (w - pool_size) // stride + 1
    # pooled_image = np.zeros((new_h, new_w))
    #
    #
    # for i in range(new_h):
    #     for j in range(new_w):
    #         pooled_image[i, j] = np.max(
    #             image_array[i * stride:i * stride + pool_size, j * stride:j * stride + pool_size])
    #
    # print(image_array/255)
    #
    # return pooled_image

    matrix_data = image_array / 255 - 0.5

    encrypted_lists = he.send_data(matrix_data=matrix_data, n=pool_size, s=stride)

    sorted_lists = he.sort_encrypt_messages(encrypted_lists)

    result = he.receive_data(sorted_lists)

    return (result + 0.5) * 255
