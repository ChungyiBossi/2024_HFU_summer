import pytest
import cv2
import mediapipe as mp
from computer_vision.image_format_converter import (
    convert_from_bytes_to_cv2,
    convert_from_cv2_to_bytes,
    convert_from_cv2_to_mediapipe_image,
    convert_from_mediapipe_image_to_cv2
)

@pytest.mark.parametrize(
    "test_case_path", [
        'tests/test_case/test.jpeg', 
    ]
)
class TestImageConvertion:
    @pytest.fixture()
    def cv_img(self, test_case_path):
        return cv2.imread(test_case_path)

    @pytest.fixture()
    def mp_img(self, test_case_path):
        return mp.Image.create_from_file(test_case_path)

    def test_convertion_between_cv2_to_bytes(self, cv_img):
        image_bytes = convert_from_cv2_to_bytes(cv_img)
        assert isinstance(image_bytes, bytes), print("cv2 to bytes fail", type(cv_img), type(image_bytes))

        cv2_img = convert_from_bytes_to_cv2(image_bytes)
        assert isinstance(cv2_img, cv2.typing.MatLike), print("bytes to cv2 fail", type(image_bytes), type(cv2_img))

    def test_convert_from_cv2_to_mediapipe_image(self, cv_img):
        mp_img = convert_from_cv2_to_mediapipe_image(cv_img)
        assert isinstance(mp_img, mp.Image), print("cv2 to PIL Image fail", type(cv_img), type(mp_img))
        
    def test_convert_from_mediapipe_image_to_cv2(self, mp_img):
        cv2_img = convert_from_mediapipe_image_to_cv2(mp_img)
        assert isinstance(cv2_img, cv2.typing.MatLike), print("cv2 to PIL Image fail", type(cv2_img), type(mp_img))
        