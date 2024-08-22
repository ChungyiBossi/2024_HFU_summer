from flask import (
    Flask, 
    request, 
    abort, 
    render_template
)
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,  # 傳輸回Line官方後台的資料格式
    ImageMessage,
    TemplateMessage, 
    ButtonsTemplate, CarouselTemplate, CarouselColumn, ConfirmTemplate,
    PostbackAction,
    MessageAction,
    URIAction,
    QuickReply, QuickReplyItem
)
from linebot.v3.webhooks import (
    MessageEvent, # 傳輸過來的方法
    TextMessageContent, # 使用者傳過來的資料格式
    ImageMessageContent,
    LocationMessageContent
)
from handle_keys import get_secret_and_token
from openai_api import chat_with_chatgpt
from data_scraper.cwa_opendata_scraper import get_cities_weather
from computer_vision.imgur_uploader import init_imgur_client, upload_to_imgur
from computer_vision.mediapipe_cv_tools import init_face_detector, detect_face_with_content_drawing
from computer_vision.image_format_converter import convert_from_cv2_to_bytes

app = Flask(__name__)
keys = get_secret_and_token()
handler = WebhookHandler(keys['LINEBOT_SECRET_KEY'])
configuration = Configuration(access_token=keys['LINEBOT_ACCESS_TOKEN'])
face_detection_model = init_face_detector('computer_vision/cv_models/blaze_face_short_range.tflite')

@app.route("/")
def say_hello_world(username=""):
    # 測試用，確定webhook server 有連通
    return render_template("hello.html", name=username)

@app.route("/callback", methods=['POST'])
def callback():
    # 設計一個 #callback 的路由，提供給Line官方後台去呼叫
    # 也就所謂的呼叫Webhook Server
    # 因為官方會把使用者傳輸的訊息轉傳給Webhook Server
    # 所以會使用 RESTful API 的 POST 方法

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # 根據不同的使用者事件(event)，用不同的方式回應
    # eg. MessageEvent 代表使用者單純傳訊息的事件
    # TextMessageContent 代表使用者傳輸的訊息內容是文字
    # 符合兩個條件的事件，會被handle_message 所處理
    user_id = event.source.user_id # 使用者的ID
    user_message = event.message.text # 使用者傳過來的訊息
    api_key = keys["OPENAI_API_KEY"]

    if '特務P天氣如何' in user_message:
        # 假定的格式: 特務P天氣如何 臺中市 桃園市 彰化市
        responses = [
            TextMessage(text=handle_weather(user_id, user_message))
        ]
    elif "按鈕sample" in user_message:
        responses = [create_buttons_template()]
    elif "輪播sample" in user_message:
        responses = [create_carousel_template()]
    elif "確認sample" in user_message:
        responses = [create_check_template()]
    elif "快速回覆sample" in user_message:
        responses = [create_quick_reply()]
    else:# 閒聊
        responses = [
            TextMessage(text=chat_with_chatgpt(user_id, user_message, api_key))
        ] 
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=responses
            )
        )

def handle_weather(user_id, user_message, chatgpt_api_key=keys['OPENAI_API_KEY']):
    # 問天氣
    cwa_api_key = keys['CWA_API_KEY']
    locations_name = user_message.split()[1:] # 取得地點 > NLP:實體辨識
    if locations_name: # 有地點才做事情
        weather_data = get_cities_weather(cwa_api_key, locations_name)
        '''
        台中市:
            xxx: aaa 
            yyy: bbb
            zzz: ccc
        '''
        response = ""
        for location in weather_data: # 取得每一個縣市的名稱
            response += f"{location}:\n" # 加入縣市名稱訊息到response
            for weather_key in sorted(weather_data[location]): # 根據縣市名稱，取得縣市天氣資料
                response += f"\t\t\t\t{weather_key}: {weather_data[location][weather_key]}\n"
        response = response.strip()
        response = chat_with_chatgpt(
            user_id, response, chatgpt_api_key,
            extra_prompt="請你幫我生出一段報導，根據前面的天氣資訊，建議使用者的穿搭等等，每個縣市分開，200字以內。"
        )
    else:
        response = "請給我你想知道的縣市，請輸入：特務P天氣如何 臺中市 桃園市 彰化市"
    return response

def create_buttons_template(menu_name='Menu', description='Please select'):
    response = ButtonsTemplate(
        title=menu_name,
        text=description,
        actions=[
            PostbackAction(
                label='postback action',
                display_text='postback text',
                data='action=buy&itemid=123'
            ),
            MessageAction(
                label='message action',
                text='message text'
            ),
            URIAction(
                label='uri action',
                uri='http://example.com/'
            )
        ]
    )
    return TemplateMessage(
        type='template',
        altText="TemplateMessage",
        template=response
    )

def create_carousel_template():
    carousel = CarouselTemplate(columns=[
        CarouselColumn(
            text='按鈕文字',
            title='按鈕標題',
            thumbnail_image_url='https://i.imgur.com/fz8h8GO.jpeg',
            actions=[
                MessageAction(label='發送文字訊息', text='我發送一個文字訊息'),
                MessageAction(label='講笑話', text='請告訴我一個笑話'),
                MessageAction(label='推薦餐廳', text='請推薦一個餐廳給我'),
            ]
        ),
        CarouselColumn(
            text='連結描述',
            title='連結標題',
            thumbnail_image_url='https://i.imgur.com/fz8h8GO.jpeg',
            actions=[
                URIAction(label='前往GOOGLE', uri='https://www.google.com'),
                URIAction(label='每個卡片的欄位', uri='https://www.google.com'),
                URIAction(label='都要一致，所以補行', uri='https://www.google.com')
            ]
        )
    ])
    return TemplateMessage(
        type='template',
        altText="TemplateMessage",
        template=carousel
    )

def create_check_template():
    response = ConfirmTemplate(
        text='您確定嗎？',
        actions=[
            MessageAction(label='是', text='Yes'),
            MessageAction(label='否', text='No')
        ]
    )
    return TemplateMessage(
        type='template',
        altText="TemplateMessage",
        template=response
    )

def create_quick_reply():
    quick_reply_body = QuickReply(items=[
        QuickReplyItem(action=MessageAction(label='否', text='No')),
        QuickReplyItem(action=MessageAction(label='否', text='No')),
        QuickReplyItem(action=URIAction(label='前往GOOGLE', uri='https://www.google.com'))
    ])

    return TextMessage(
        text="超快速回覆",
        quickReply=quick_reply_body
        
    )

@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image(event):
    # 取得圖片
    image_id = event.message.id
    image_url = f'https://api-data.line.me/v2/bot/message/{image_id}/content'
    header = {
        'Authorization': f'Bearer {keys['LINEBOT_ACCESS_TOKEN']}'
    }
    
    temp_image_path = 'image_message.jpeg'
    response = requests.get(image_url, headers=header)
    if response.status_code == 200: # 取圖片 > 視覺處理 > 存圖
        # 跑 mediapipe face detection
        detected_frame = detect_face_with_content_drawing(
            face_detection_model, image_content=response.content
        )
        # 存圖片
        frame_in_bytes = convert_from_cv2_to_bytes(detected_frame)
        with open(temp_image_path, 'wb') as image_file:
            image_file.write(frame_in_bytes)
        response = 'Get image success.'
    else:
        response = 'Get image failed.'

    # imgur upload
    imgur_client = init_imgur_client(keys['IMGUR_CLIENT_ID'], keys['IMGUR_SECRET_KEY'])
    imgur_link = upload_to_imgur(temp_image_path, imgur_client)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=response),
                    ImageMessage(
                        originalContentUrl=imgur_link,
                        previewImageUrl=imgur_link
                    )
                ]
            )
        )

if __name__ == "__main__":
    app.run(debug=True)