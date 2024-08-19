import mediapipe as mp # 通常會縮寫成mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision

# 實際上工作的類別
GestureRecognizer = mp.tasks.vision.GestureRecognizer 
# 不同模型間都有的基礎設定，eg: 模型路徑
BaseOptions = mp.tasks.BaseOptions 
# 工作類別的進階設定，每種模型可能會不同
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions 
# 輸入設定，算是進階設定的一個欄位
VisionRunningMode = mp.tasks.vision.RunningMode

# 讀model binary content: https://github.com/google-ai-edge/mediapipe/issues/5343
model_path = 'gesture_recognizer.task'
with open(model_path, 'rb') as model: # 建立檔案和程式碼的通道
    model_file = model.read()

# 組合你的各種設定
options = GestureRecognizerOptions(
    base_options=BaseOptions(
        model_asset_buffer=model_file), # 直接讀模型的binary內容，丟給物件。
    running_mode=VisionRunningMode.IMAGE)

with GestureRecognizer.create_from_options(options) as recognizer:
    # Load the input image from an image file.
    mp_image = mp.Image.create_from_file('images/victory_1.jpg')
    # 手勢辨識
    gesture_recognition_result = recognizer.recognize(mp_image)

    # print result
    top_gesture = gesture_recognition_result.gestures[0][0]
    hand_landmarks = gesture_recognition_result.hand_landmarks[0]
    print("Top Gesture: ", top_gesture.category_name, top_gesture.score)
    for landmark in hand_landmarks:
        print("Landmark: ", round(landmark.x, 3), round(landmark.y, 3), round(landmark.z, 3))
    