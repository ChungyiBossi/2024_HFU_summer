
### Goal: 
讓Teachable Machine訓練的模型，可以在本地使用 = 可以給flask server 使用
1. 先到Teachable Machine訓練並測試你的模型
2. 下載你的模型跟範例程式碼
    * 專案類型選擇 Tensorflow
    * 模型轉換選擇 Savedmodel，並下載模型。
        > 下載後解壓縮，把裡面的資料丟到你的開發環境裏頭。
    * 範例選擇 OpenCV Keras
3. 安裝 pip package
    * pip install opencv-python
    * pip install tensorflow~=2.16.1
4. [執行python範例程式碼]()
5. (可選) 把模型檔案加入到.gitignore
    



#### Trouble Shooting
* [Keras 匯出模型會遇到問題](https://stackoverflow.com/questions/78187204/trying-to-export-teachable-machine-model-but-returning-error)