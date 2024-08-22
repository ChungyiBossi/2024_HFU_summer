import cv2
import numpy as np
from image_format_converter import convert_from_bytes_to_cv2, convert_from_cv2_to_bytes

if __name__ == '__main__':
    with open('test.jpg', 'rb') as file:
        byte_data = file.read()

    cv2_image = convert_from_bytes_to_cv2(byte_data)
    image_bytes = convert_from_cv2_to_bytes(cv2_image)

    with open('test_write.jpg', 'wb') as out:
        out.write(image_bytes)