from PIL import Image
import numpy as np
import utils

def process_image(image_path, pool_size, stride):
    image = Image.open(image_path).convert('L')  # 회색조로 변환
    image_array = np.array(image)

    pooled_image_array = utils.max_pooling(image_array, pool_size, stride)
    pooled_image = Image.fromarray(pooled_image_array.astype('uint8'))

    return pooled_image
