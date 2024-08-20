import mediapipe as mp
import cv2
from image_collector import put_cv2_text

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
        running_mode=VisionRunningMode.IMAGE
    )
    return GestureRecognizer.create_from_options(options)

def recognize_gesture(cv2_frame):
    # https://ai.google.dev/edge/api/mediapipe/python/mp/Image
    # cv2 frame -> mp.Image
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2_frame)
    # 手勢辨識
    gesture_recognition_result = model.recognize(mp_image)
    # print result
    top_gesture = gesture_recognition_result.gestures
    if top_gesture: # 是否有辨識出手勢
        top_gesture = top_gesture[0][0]
        print("Top Gesture: ", top_gesture.category_name, top_gesture.score)
        return top_gesture.category_name, top_gesture.score
    else: # 沒有辨識出手勢
        print("No Gesture")
        return "None", 1.0
    
def recognize_gesture_realtime(model, camera_id):
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
                top_gesture, score = recognize_gesture(frame)
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

if __name__ == '__main__':
    model_path = 'gesture_recognizer.task'
    camera_id = 1
    model = init_gesture_recognizer(model_path)
    recognize_gesture_realtime(model, camera_id)