import numpy as np
from heaan_utils import HEAAN

he = HEAAN()
he.initialize()


def max_pooling(image_array, pool_size, stride):
    # 이미지 배열을 [0, 1] 범위로 정규화하고, [-0.5, 0.5] 범위로 이동
    matrix_data = image_array / 255 - 0.5

    # 매트릭스를 윈도우 사이즈와 스트라이드로 나누고, 각각을 암호화하여 서버에 전송
    encrypted_lists = he.send_data(matrix_data=matrix_data, n=pool_size, s=stride)

    # 서버에서 각 윈도우 내의 암호화된 값을 내림차순으로 정렬
    sorted_lists = he.sort_encrypt_messages(encrypted_lists)

    # 정렬된 결과를 서버로부터 수신하고 복호화하여 최대 풀링 결과 생성
    result = he.receive_data(sorted_lists)

    # 결과를 다시 [0, 255] 범위로 변환하여 반환
    return (result + 0.5) * 255


def approx_max_pooling(image_array, pool_size, stride):
    # 이미지 배열을 [0, 1] 범위로 정규화하고, [-0.5, 0.5] 범위로 이동
    matrix_data = image_array / 255 - 0.5

    # 매트릭스를 윈도우 사이즈와 스트라이드로 나누고, 각각을 암호화하여 서버에 전송 (근사화를 이용한 방식)
    encrypted_lists = he.send_data_approx(matrix_data=matrix_data, n=pool_size, s=stride)

    # 서버에서 각 윈도우 내의 암호화된 값을 근사화하여 최대값을 찾음
    sorted_lists = he.max_encrypt_messages(encrypted_lists)

    # 근사화된 최대값을 서버로부터 수신하고 복호화하여 최대 풀링 결과 생성
    result = he.receive_data(sorted_lists)

    # 결과를 절대값으로 변환하고 [0, 255] 범위로 변환하여 반환
    return abs((result + 0.5) * 255 * 2)
