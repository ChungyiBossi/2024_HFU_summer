import mediapipe as mp # 通常會縮寫成mp

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
    mp_image = mp.Image.create_from_file('images/victory_2.jpg')
    # 手勢辨識
    gesture_recognition_result = recognizer.recognize(mp_image)

    # print result
    top_gesture = gesture_recognition_result.gestures
    hand_landmarks = gesture_recognition_result.hand_landmarks
    if top_gesture and hand_landmarks: # 是否有判斷出手勢 & 判斷出手
        top_gesture = top_gesture[0][0]
        hand_landmarks = hand_landmarks[0]
        print("Top Gesture: ", top_gesture.category_name, top_gesture.score)
        for landmark in hand_landmarks:
            print("Landmark: ", round(landmark.x, 3), round(landmark.y, 3), round(landmark.z, 3))

# 目的：把拿到的手指節點(hand landmarks)，以及點跟點之間的連結，畫在圖上
import cv2
from mediapipe.framework.formats import landmark_pb2 # 型態轉換

# 繪圖設定(22-24)
mp_hands = mp.solutions.hands  # 手部的一些設定
mp_drawing = mp.solutions.drawing_utils # 繪畫的設定
mp_drawing_styles = mp.solutions.drawing_styles # 線條的風格

# 型態轉換 (63-66)
hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
hand_landmarks_proto.landmark.extend([
    landmark_pb2.NormalizedLandmark(
        x=landmark.x, y=landmark.y, z=landmark.z
    ) 
    for landmark in hand_landmarks
])

# 把MediaPipe(pillow)圖片 --> cv2 image (numpy array)
# https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
annotate_image = mp_image.numpy_view()[:, :, ::-1].copy()

# (68-73)
mp_drawing.draw_landmarks(
    annotate_image,
    hand_landmarks_proto,
    mp_hands.HAND_CONNECTIONS,
    # mp_drawing_styles.get_default_hand_landmarks_style(),
    # mp_drawing_styles.get_default_hand_connections_style()
)

# 利用opencv顯示圖片到視窗
cv2.imshow("Hands", annotate_image)
key = cv2.waitKey(200000)
if key == ord('q'):
    cv2.destroyAllWindows()
cv2.destroyAllWindows()