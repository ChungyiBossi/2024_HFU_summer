import cv2
import time

def put_cv2_text(image, text, org):
    cv2.putText( 
        img=image,
        text=text,
        org=org,  # 圖片的像素坐標系，Y軸是反過來的(向下變大)
        fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
        fontScale=1,
        color=(0, 255, 255), 
        thickness=5, 
        lineType=cv2.LINE_AA
    )            

def collect_image(folder_path, category_name, camera_id):
    window_name = "Collector"
    camera = cv2.VideoCapture(camera_id)
    is_collection_start = False # 預設不會一開始就蒐集
    while True:
        is_success, frame = camera.read()  # 從camera取得資料
        if is_success:
            # 我想要在這邊可以透過camera蒐集圖片
            show_frame = frame.copy() # Copy frame for display
            put_cv2_text(show_frame, f"Collecting: {is_collection_start}", (30, 50)) # 顯示出是否蒐集中?
            put_cv2_text(show_frame, f"Category: {category_name}", (30, 100)) # 顯示出蒐集類別?
            cv2.imshow(window_name, show_frame)
            if is_collection_start: # 要蒐集
                image_name = f"{time.time()}.jpg" # 我用 timestamp
                filename = f"{folder_path}/{category_name}/{image_name}" # 組合檔名
                cv2.imwrite(filename, frame)
                key = cv2.waitKey(100)
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
    cv2.destroyWindow(window_name)
    
if __name__ == '__main__':
    camera_id = 0
    folder_path = 'images/gesture'
    categories_name = ['open_palm', 'thumb_up', 'victory']
    for category_name in categories_name:
        collect_image(folder_path, category_name, camera_id)