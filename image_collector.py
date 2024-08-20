import cv2
camera = cv2.VideoCapture(0)
while True:
    is_success, frame = camera.read()  # 從camera取得資料
    if is_success:
        # 我想要在這邊可以透過camera蒐集圖片
        cv2.imshow("Collector", frame)
        cv2.imwrite("image.jpg", frame)
        key = cv2.waitKey(100)
    else:
        print("Wait for camera ready......")
        key = cv2.waitKey(1000)

    if key == ord('q') or \
       key == ord("Q"): # 如果按下'q' or 'Q'
        break

cv2.destroyAllWindows() # close all window
    