# Goal: 學會如何使用Mediapipe這類的大型開源軟體，並應用在實務上

0. Mediapipe是Google開源的AI邊緣運算函式庫，有一定的效果與不吃硬體的效能。
1. 從線上Demo初步了解此軟體能達成甚麼功能? 以及個別功能的輸入輸出與限制。
    * 電腦視覺相關，包含但不只以下:
        * 手部 - 整隻手的辨識(detection)，手的節點識別(recognization)，手勢的識別，手的追蹤(tracking)
        * 臉部 - 人臉辨識(哪裡有人)，人臉識別(是誰)，臉部的節點識別(眉心 or 嘴角)，五官識別
        * 姿勢 - 全身節點的識別(大關節)
    * 文字相關
    * 聲音相關
2. 查閱相關的[文檔](https://developers.google.com/mediapipe)
3. 嘗試 [範例程式碼](https://mediapipe-studio.webapps.google.com/demo/gesture_recognizer?hl=zh-tw)

4. 改成你實際應用的情境，通常會是realtime的，會更符合邊緣裝置的情境
    * 圖片格式有分 pillow 和 numpy，兩者的格式不同，類似.mp3與.wav，會需要轉檔
        > mediapipe.Image 底層使用 pillow

        > cv2.mat 是 numpy 格式
    * 需要利用opencv讀取鏡頭資料，故會需要轉換 cv2.mat -> mp.Image
    * 轉成 mp.Image 後，就能夠丟給模型物件去使用。

5. 嘗試去組合多種的功能，用一個合理的情境包裝。