from PIL import Image
import numpy as np
import utils


def process_image(image_path, pool_size, stride):
    try:
        image = Image.open(image_path).convert('L')  # Convert to grayscale
        image_array = np.array(image)

        # Perform max pooling
        pooled_image_array = utils.max_pooling(image_array, pool_size, stride)

        # Calculate the dimensions of the pooled image without padding
        original_h, original_w = image_array.shape
        pooled_h = (original_h - pool_size) // stride + 1
        pooled_w = (original_w - pool_size) // stride + 1

        # Slice the pooled_image_array to remove padding
        sliced_pooled_image_array = pooled_image_array[:pooled_h, :pooled_w]

        # Convert to image
        pooled_image = Image.fromarray(sliced_pooled_image_array.astype('uint8'))

        return sliced_pooled_image_array, pooled_image
    except Exception as e:
        print(f"Error processing image: {e}")
        raise
