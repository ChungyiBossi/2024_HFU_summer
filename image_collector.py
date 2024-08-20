import cv2
import time

folder_path = 'images/gesture'
category_name = 'open_palm'
camera = cv2.VideoCapture(1)
is_collection_start = False # 預設不會一開始就蒐集
while True:
    is_success, frame = camera.read()  # 從camera取得資料
    if is_success:
        # 我想要在這邊可以透過camera蒐集圖片
        cv2.imshow("Collector", frame)
        if is_collection_start: # 要蒐集
            image_name = f"{time.time()}.jpg" # 我用 timestamp
            filename = f"{folder_path}/{category_name}/{image_name}" # 組合檔名
            cv2.imwrite(filename, frame)
            key = cv2.waitKey(500)
        else: # 不蒐集
            key = cv2.waitKey(1)
    else:
        print("Wait for camera ready......")
        key = cv2.waitKey(1000)

    if key == ord('q') or key == ord("Q"): # 中止
        break
    elif key == ord('a') or key == ord('A'): # 開始
        is_collection_start = True
    elif key == ord('z') or key == ord('Z'): # 暫停
        is_collection_start = False

cv2.destroyAllWindows() # close all window
    