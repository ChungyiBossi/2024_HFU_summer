# 2024 夏 台中新尖兵
> Goal: 學習機器學習應用，並實際製作小組專題

## 開發環境管理
> 建立虛擬環境以利管理 Python Package
* [虛擬環境建立](./workflow/虛擬環境建立流程.md)

* [新電腦/雲端/團隊協作時，重建環境](./workflow/重建環境的流程.md)

* [自動化測試部屬；Github Actiions CI/CD](./workflow/github_actions_CICD.md)

## **爬蟲**
> 蒐集網路資料，API或動靜態爬蟲都是可能的方式

* [台灣中央氣象局(CWA)爬蟲流程](workflow/中央氣象局爬蟲流程.md)
* [靜態爬蟲 BeautifulSoup- 資安大會參展廠商列表](data_scraper/cybersec_exhibition_info.py)
* [動態爬蟲 Selenium - 資安大會特定廠商資訊](data_scraper/cybersec_scraper.ipynb)

### Chatbot UI
> 用以呈現爬蟲成果，以Linebot為介面，以ChatGPT 生成文字

### Linebot
> 後端為Flask Webhook Server，用NGROK forwarding到公開網路上

* [Linebot + NGROK + Flask Webhook Server](workflow/Line與ngrok與Flask後端的三方串接.md)
* [Linebot Event Sample](./create_linebot_messages_sample.py)

### ChatGPT
> 利用ChatGPT + Pre-define Prompt，生成較不死板的回覆

> 需要先 [申請 OpenAI API Key](https://platform.openai.com/api-keys)

* [ChatGPT NLG with convesation history](./workflow/OpenAI對話生成.md)


## 電腦視覺
讓電腦能夠自動化處理影像資料，主要分為以下幾種應用：
1. 圖像分類，有可圖形化的[Teachable Machine](./workflow/teachable_machine_workflow.md)可直接應用
2. 物件/人體偵測 (detection)
3. 物件/人體追蹤 (tracking)
4. 臉部/手部/全身 Landmarks 節點辨識 (Recognize)
5. 特定領域的辨識，eg. 利用手部Landmarks做的[手勢辨識](https://mediapipe-studio.webapps.google.com/demo/gesture_recognizer?hl=zh-tw)

> [偵測/追蹤/辨識 可以參考 Mediapipe](./workflow/Mediapipe使用流程.md)

> [基於 Mediapipe + OpenCV 的第三方資源：CVZONE](https://www.computervision.zone/courses/learn-computer-vision-with-cvzone/)