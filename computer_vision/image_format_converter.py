import numpy as np
from PIL import Image
import cv2


def convert_from_cv2_to_image(img: np.ndarray) -> Image:
    # return Image.fromarray(img)
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    # return np.asarray(img)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def convert_from_bytes_to_cv2(data:bytes) -> cv2.Mat: # 將字節數據轉換為 NumPy 數組
    nparr = np.frombuffer(data, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

def convert_from_cv2_to_bytes(img: cv2.Mat) -> bytes:
    # OpenCV 圖像 -> 可open(...) 寫入的圖像
    res, image = cv2.imencode('.jpeg', img)
    assert res, print('Fail to convert cv2.Mat to ndarray')
    return image.tobytes()