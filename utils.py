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
    matrix_data = image_array/255

    encrypted_lists = he.send_data(matrix_data=matrix_data, n=pool_size, s=stride)

    sorted_lists = he.max_encrypt_messages(encrypted_lists)

    result = he.receive_data(sorted_lists)
    return result * 255

# matrix = [
#     [255.0, 200.0, 200.0, 200.0],
#     [180.0, 160.0, 144.0, 245.0],
#     [9.0, 10.0, 11.0, 12.0],
#     [13.0, 14.0, 15.0, 16.0]
# ]

matrix = [
    [255.0, 200.0],
    [180.0, 160.0]
]


matrix = np.array(matrix)
print(matrix)

window_size = 2
stride = 2

# 암호화 과정
encrypted_data = approx_max_pooling(matrix, window_size, stride)
print(encrypted_data)
#
# # Approximate Max 계산
# approx_max_result = approx_max(encrypted_data[0], 2)
# approx_max_result = he.decrypt_message(approx_max_result)
# print("Approximate Max Result:", abs(approx_max_result[0]-255))


# def approx_max_pooling(image_array, pool_size, stride):
#     matrix_data = image_array
#     encrypted_lists = he.send_data(matrix_data=matrix_data, n=pool_size, s=stride)

