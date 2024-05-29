import numpy as np

def max_pooling(image_array, pool_size, stride):
    h, w = image_array.shape
    new_h = (h - pool_size) // stride + 1
    new_w = (w - pool_size) // stride + 1
    pooled_image = np.zeros((new_h, new_w))

    for i in range(new_h):
        for j in range(new_w):
            pooled_image[i, j] = np.max(image_array[i*stride:i*stride+pool_size, j*stride:j*stride+pool_size])

    return pooled_image
