import mediapipe as mp # 通常會縮寫成mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = 'gesture_recognizer.task'
# 實際上工作的類別
GestureRecognizer = mp.tasks.vision.GestureRecognizer 
# 不同模型間都有的基礎設定，eg: 模型路徑
BaseOptions = mp.tasks.BaseOptions 
# 工作類別的進階設定，每種模型可能會不同
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions 
# 輸入設定，算是進階設定的一個欄位
VisionRunningMode = mp.tasks.vision.RunningMode

# 組合你的各種設定
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE)

with GestureRecognizer.create_from_options(options) as recognizer:
    # Load the input image from an image file.
    mp_image = mp.Image.create_from_file('images/victory_1.jpg')
    # 手勢辨識
    gesture_recognition_result = recognizer.recognize(mp_image)

    # print result
    print(gesture_recognition_result)
    