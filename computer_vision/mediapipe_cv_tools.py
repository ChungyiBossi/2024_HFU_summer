import mediapipe as mp
import cv2
import numpy as np
try:
    from .image_collector import put_cv2_text
    from .image_format_converter import convert_from_bytes_to_cv2, convert_from_cv2_to_mediapipe_image, convert_from_mediapipe_image_to_cv2
except Exception:
    from image_collector import put_cv2_text
    from image_format_converter import convert_from_bytes_to_cv2, convert_from_cv2_to_mediapipe_image, convert_from_mediapipe_image_to_cv2
from mediapipe.framework.formats import landmark_pb2 # 型態轉換
mp_hands = mp.solutions.hands  # 手部的一些設定
mp_drawing = mp.solutions.drawing_utils # 繪畫的設定
mp_drawing_styles = mp.solutions.drawing_styles # 線條的風格

mp_poses = mp.solutions.pose.POSE_CONNECTIONS

def draw_landmark(cv_image, landmarks, connection): # 畫 landmarks
    hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    hand_landmarks_proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(
            x=landmark.x, y=landmark.y, z=landmark.z
        ) 
        for landmark in landmarks
    ])

    mp_drawing.draw_landmarks(
        cv_image,
        hand_landmarks_proto,
        connection
    )
    cv2.imshow("landmarks", cv_image)

def init_gesture_recognizer(model_path): # 初始化你的手勢辨識模型
    # 實際上工作的類別
    GestureRecognizer = mp.tasks.vision.GestureRecognizer 
    # 不同模型間都有的基礎設定，eg: 模型路徑
    BaseOptions = mp.tasks.BaseOptions 
    # 工作類別的進階設定，每種模型可能會不同
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions 
    # 輸入設定，算是進階設定的一個欄位
    VisionRunningMode = mp.tasks.vision.RunningMode
    # 讀model binary content: https://github.com/google-ai-edge/mediapipe/issues/5343
    with open(model_path, 'rb') as model: # 建立檔案和程式碼的通道
        model_file = model.read()
    # 組合你的各種設定
    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_buffer=model_file), # 直接讀模型的binary內容，丟給物件。
        running_mode=VisionRunningMode.IMAGE,
        min_hand_detection_confidence=0.3,
        # min_hand_presence_confidence
    )
    return GestureRecognizer.create_from_options(options)

def recognize_gesture(model, cv2_frame, is_drawing=True): # 使用模型辨識，並輸出結果
    mp_image = convert_from_cv2_to_mediapipe_image(cv2_frame)
    # 手勢辨識
    gesture_recognition_result = model.recognize(mp_image)
    # print result
    top_gesture = gesture_recognition_result.gestures
    hand_landmarks = gesture_recognition_result.hand_landmarks
    if top_gesture and hand_landmarks: # 是否有辨識出手勢
        top_gesture = top_gesture[0][0]
        print("Top Gesture: ", top_gesture.category_name, top_gesture.score)
        if is_drawing:
            draw_landmark(
                cv2_frame, 
                hand_landmarks[0], 
                mp_hands.HAND_CONNECTIONS
            )
        return top_gesture.category_name, top_gesture.score
    else: # 沒有辨識出手勢
        print("No Gesture")
        return "None", 1.0
    
def recognize_gesture_realtime(model, camera_id): # 動態取得攝像頭擷取，送給模型辨識並畫圖
    window_name = "Gesture Recognization"
    camera = cv2.VideoCapture(camera_id)
    is_collection_start = False # 預設不會一開始就蒐集
    while True:
        is_success, frame = camera.read()  # 從camera取得資料
        if is_success:
            show_frame = frame.copy() # Copy frame for display
            put_cv2_text(show_frame, f"Collecting: {is_collection_start}", (30, 50)) # 顯示出是否蒐集中?
            if is_collection_start: # 要蒐集
                # 辨識手勢
                top_gesture, score = recognize_gesture(model, frame)
                put_cv2_text(show_frame, f"Category: {top_gesture} - {round(score*100, 2)}%", (30, 100)) # 顯示出蒐集類別?
                key = cv2.waitKey(100)
            else: # 不蒐集
                key = cv2.waitKey(1)
            cv2.imshow(window_name, show_frame)
        else:
            print("Wait for camera ready......")
            key = cv2.waitKey(1000)

        if key == ord('q') or key == ord("Q"): # 中止
            break
        elif key == ord('a') or key == ord('A'): # 開始
            is_collection_start = True
        elif key == ord('z') or key == ord('Z'): # 暫停
            is_collection_start = False
    cv2.destroyWindow(window_name)

def init_face_detector(model_path):
    FaceDetector = mp.tasks.vision.FaceDetector
    FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
    BaseOptions = mp.tasks.BaseOptions 
    VisionRunningMode = mp.tasks.vision.RunningMode
    with open(model_path, 'rb') as model:
        model_file = model.read()
    # 組合你的各種設定
    options = FaceDetectorOptions(
        base_options=BaseOptions(model_asset_buffer=model_file),
        running_mode=VisionRunningMode.IMAGE
    )
    return FaceDetector.create_from_options(options)

def detect_face(model, cv2_frame):
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2_frame)
    face_detection_result = model.detect(mp_image)
    return face_detection_result.detections

def detect_face_with_content_drawing(model, image_content): # 針對一張圖的臉部偵測，可畫圖
    if type(image_content) == bytes: # 做 byte -> cv2.Mat(opencv的image)
        image_content = convert_from_bytes_to_cv2(image_content)
    
    detections = detect_face(model, image_content)
    for detection in detections:
        bbox = detection.bounding_box
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        cv2.rectangle(image_content, start_point, end_point, (0, 255, 255), 3)
    return image_content # 畫好的圖

def detect_face_realtime(model, camera_id):
    window_name = "Face Detection"
    camera = cv2.VideoCapture(camera_id)
    is_collection_start = False # 預設不會一開始就蒐集
    while True:
        is_success, frame = camera.read()  # 從camera取得資料
        if is_success:
            show_frame = frame.copy() # Copy frame for display
            put_cv2_text(show_frame, f"Collecting: {is_collection_start}", (30, 50)) # 顯示出是否蒐集中?
            if is_collection_start: # 要蒐集
                detections = detect_face(model, frame)
                for detection in detections:
                    # Draw bounding_box
                    bbox = detection.bounding_box
                    start_point = bbox.origin_x, bbox.origin_y # 左上錨點
                    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height # 右下錨點
                    cv2.rectangle(show_frame, start_point, end_point, (0, 255, 255), 3)
                key = cv2.waitKey(100)
            else: # 不蒐集
                key = cv2.waitKey(1)
            cv2.imshow(window_name, show_frame)
        else:
            print("Wait for camera ready......")
            key = cv2.waitKey(1000)

        if key == ord('q') or key == ord("Q"): # 中止
            break
        elif key == ord('a') or key == ord('A'): # 開始
            is_collection_start = True
        elif key == ord('z') or key == ord('Z'): # 暫停
            is_collection_start = False
    cv2.destroyWindow(window_name)

if __name__ == '__main__':
    camera_id = 0
    
    # Gesture
    model_path = 'cv_models/gesture_recognizer.task'
    gesture_model = init_gesture_recognizer(model_path)
    recognize_gesture_realtime(gesture_model, camera_id)

    # # Face
    # model_path = 'cv_models/blaze_face_short_range.tflite'
    # face_detection_model = init_face_detector(model_path)
    # # detect_face_realtime(face_detection_model, camera_id) # real-time detection

    # with open("test.jpeg", "rb") as image_content: # single image detection
    #     output = detect_face_with_content_drawing(face_detection_model, image_content.read())
    #     output_bytes = convert_from_cv2_to_bytes(output)
    #     with open('test_out.jpeg', 'wb') as file:
    #         file.write(output_bytes)

    cv2.destroyAllWindows()