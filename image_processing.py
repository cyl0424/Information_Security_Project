from PIL import Image
import numpy as np
import utils


def process_image(image_path, pool_size, stride):
    try:
        image = Image.open(image_path).convert('L')  # Convert to grayscale
        image_array = np.array(image)

        # Perform max pooling
        pooled_image_array = utils.max_pooling(image_array, pool_size, stride)

        # Ensure the array is real
        if np.iscomplexobj(pooled_image_array):
            pooled_image_array = np.real(pooled_image_array)

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


def process_image_rgb(image_path, pool_size, stride):
    try:
        image = Image.open(image_path).convert('RGB')  # Keep the image in RGB mode
        image_array = np.array(image)

        # Separate the color channels
        red_channel = image_array[:, :, 0]
        green_channel = image_array[:, :, 1]
        blue_channel = image_array[:, :, 2]

        # Perform max pooling on each channel
        pooled_red = utils.max_pooling(red_channel, pool_size, stride)
        pooled_green = utils.max_pooling(green_channel, pool_size, stride)
        pooled_blue = utils.max_pooling(blue_channel, pool_size, stride)

        # Ensure the arrays are real
        if np.iscomplexobj(pooled_red):
            pooled_red = np.real(pooled_red)
        if np.iscomplexobj(pooled_green):
            pooled_green = np.real(pooled_green)
        if np.iscomplexobj(pooled_blue):
            pooled_blue = np.real(pooled_blue)

        # Calculate the dimensions of the pooled image without padding
        original_h, original_w = red_channel.shape
        pooled_h = (original_h - pool_size) // stride + 1
        pooled_w = (original_w - pool_size) // stride + 1

        # Slice the pooled channels to remove padding
        sliced_pooled_red = pooled_red[:pooled_h, :pooled_w]
        sliced_pooled_green = pooled_green[:pooled_h, :pooled_w]
        sliced_pooled_blue = pooled_blue[:pooled_h, :pooled_w]

        # Stack the pooled channels back into a color image
        sliced_pooled_image_array = np.stack((sliced_pooled_red, sliced_pooled_green, sliced_pooled_blue), axis=-1)

        # Convert to image
        pooled_image = Image.fromarray(sliced_pooled_image_array.astype('uint8'))

        return sliced_pooled_image_array, pooled_image
    except Exception as e:
        print(f"Error processing image: {e}")
        raise

