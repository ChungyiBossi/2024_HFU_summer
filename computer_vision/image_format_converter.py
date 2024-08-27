import numpy as np
import mediapipe as mp
import cv2
# from PIL import Image
def convert_from_cv2_to_mediapipe_image(img: np.ndarray) -> mp.Image:
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)

def convert_from_mediapipe_image_to_cv2(img: mp.Image) -> cv2.typing.MatLike:
    return cv2.cvtColor(img.numpy_view(), cv2.COLOR_RGB2BGR)

def convert_from_bytes_to_cv2(data:bytes) -> cv2.typing.MatLike: # 將字節數據轉換為 NumPy 數組
    nparr = np.frombuffer(data, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

def convert_from_cv2_to_bytes(img: cv2.Mat) -> bytes:
    # OpenCV 圖像 -> 可open(...) 寫入的圖像
    res, image = cv2.imencode('.jpeg', img)
    assert res, print('Fail to convert cv2.Mat to ndarray')
    return image.tobytes()

if __name__ == '__main__':
    img = cv2.imread('test.jpeg')

    image_bytes = convert_from_cv2_to_bytes(img)
    assert isinstance(image_bytes, bytes), print("cv2 to bytes fail", type(img), type(image_bytes))
    
    cv2_img = convert_from_bytes_to_cv2(image_bytes)
    assert isinstance(cv2_img, cv2.typing.MatLike), print("bytes to cv2 fail", type(image_bytes), type(cv2_img))
    
    mp_img = convert_from_cv2_to_mediapipe_image(cv2_img)
    assert isinstance(mp_img, mp.Image), print("cv2 to PIL Image fail", type(cv2_img), type(mp_img))
    
    cv2_img = convert_from_mediapipe_image_to_cv2(mp_img)
    assert isinstance(cv2_img, cv2.typing.MatLike), print("cv2 to PIL Image fail", type(cv2_img), type(mp_img))

    print("All Convertion Success!")