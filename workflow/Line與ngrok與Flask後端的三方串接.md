[流程圖請詳見](https://drive.google.com/file/d/1mSC3N44GvL2fIoMkf-0FcNB0d_3kkpM1/view?usp=drive_link)

### 角色
1. Ngrok：介於**Line官方**與**你的Webhook後端**的"總機"，負責轉接。
2. Line官方：負責接收使用者端的資訊，跟總機溝通的"櫃台"。
3. Flask Webhook後端：真正處理訊息，並生成回覆的"分機"

### 步驟
> 分別為三個角色描述流程
1. Ngrok
    * [申請Ngrok帳號](https://ngrok.com/)
    * 下載 Ngrok.exe，並且把它放到你的開發資料夾內。
    * 設定你的 Ngrok auth token，將用來驗證"分機"與"總機"的連線憑證
        > ./ngrok config add-authtoken YOUR_AUTH_TOKEN
    * 讓"總機" 運作，轉接你的"分機"，Flask預設會開啟在5000
        > ./ngrok http 5000 
    * 取得你的Forwording網址，要丟給"櫃台"讓他做連接。

2. Line Develop
    * 將Ngrok提供的網址，貼到 Webhook URL 的設定內。
        > https://xxxxxxxxx/route_name
    * Verify 確定有通，有通會出現 Success 的字樣。

3. Flask Webhook Server
    * 請參考你的程式碼：
        * 先到Line Developer Console，把 Channel Secret & Channel Access Token複製起來
        * 把這兩個密文，存到環境變數內；工具列搜尋<環境變數>，新增兩個環境變數，並且把值貼上去
        * 按下確定儲存，要記得你的變數名稱，這些資訊只會存在你當前使用的電腦裡。
    * 把 debug mode打開：
        ```python
            app.run(debug=True)
        ```
    * 修改你的程式碼，調整回覆結果

    