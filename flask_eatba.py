from flask import (
    Flask, 
    request, 
    abort, 
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
)
from linebot.v3.webhooks import (
    MessageEvent, # 傳輸過來的方法
    PostbackEvent,
    TextMessageContent, # 使用者傳過來的資料格式\
)
import pandas as pd
from handle_keys import get_secret_and_token
from urllib.parse import parse_qsl
from import_modules import *
from create_linebot_messages_sample import *

app = Flask(__name__)
keys = get_secret_and_token()
handler = WebhookHandler(keys['LINEBOT_SECRET_KEY'])
configuration = Configuration(access_token=keys['LINEBOT_ACCESS_TOKEN'])

rest_recommand_memory = dict()  # 使用者選項暫存記憶

rest_dict = {
    'breakfast_rest': pd.read_csv('taichungeatba/breakfast_rest.csv').dropna(axis=1).groupby('區域'),
    'lunch_rest': pd.read_csv('taichungeatba/lunch_rest.csv').dropna(axis=1).groupby('區域'),
    'dinner_rest': pd.read_csv('taichungeatba/dinner_rest.csv').dropna(axis=1).groupby('區域')
}

@app.route("/callback", methods=['POST'])
def callback():
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
    user_id = event.source.user_id
    user_message = event.message.text # 使用者傳過來的訊息

    if "sample" in user_message:
        responses = [handle_sample(user_message)]
    elif '美食推薦' in user_message: # Get Time
        responses = [handle_choose_type()]
    elif user_message.startswith('#') and user_message.endswith('餐'): # Get Section
        responses = [handle_choose_section(user_id, user_message)]
    elif user_message.startswith('#') and user_message.endswith('區'): # Get recommand
        section_name = user_message[1:]
        responses = [handle_rests_recommand(user_id, section_name)]
    else:# 閒聊
        responses = [TextMessage(text='Got it!')] 
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=responses
            )
        )

def handle_choose_type():
    response = ButtonsTemplate(
        title='都幾!!',
        text='請選擇要推薦早餐，午餐，還是晚餐。',
        actions=[
            MessageAction(text='#早餐', label='來去吃早餐'),
            MessageAction(text='#午餐', label='來去吃午餐'),
            MessageAction(text='#晚餐', label='來去吃晚餐')
        ]
    )
    return TemplateMessage(
        type='template',
        altText="TemplateMessage",
        template=response
    )

def handle_choose_section(user_id, time_message, top_n=10):
    def create_quick_reply_item(section_name):
        return QuickReplyItem(action=MessageAction(text=f'#{section_name}', label=f'{section_name}'))

    if time_message == '#早餐':
        rest_groups = rest_dict['breakfast_rest']
    elif time_message == '#午餐':
        rest_groups = rest_dict['lunch_rest']
    elif time_message == '#晚餐':
        rest_groups = rest_dict['dinner_rest']
    
    rest_recommand_memory[user_id] = rest_groups
    sorted_sections_group_by_size = rest_groups.size().sort_values(ascending=False)
    sorted_sections = sorted_sections_group_by_size.head(top_n).index.to_list()
    quick_reply_items = [create_quick_reply_item(section) for section in sorted_sections]
    quick_reply_body = QuickReply(items=quick_reply_items)

    return TextMessage(
        text="請選擇你的所在區域~",
        quickReply=quick_reply_body
    )

def handle_rests_recommand(user_id, section_name):
    def create_rest_col(rest_title, rest_text, rest_comment=""):
        url = 'https://www.google.com'
        comment = rest_comment if rest_comment else '這是評論'
        text_for_postback = f"comment={comment}"
        return CarouselColumn(
            title=rest_title,
            text=rest_text,
            thumbnail_image_url='https://i.imgur.com/fz8h8GO.jpeg',
            actions=[
                PostbackAction(
                    label='餐廳評價',
                    displayText='取得餐廳評價',
                    data=text_for_postback
                ),
                URIAction(label='餐廳頁面', uri=url),
            ]
        )
    def get_group_sample(group):
        group_size = len(group)
        return group.sample(min(group_size, 3))

    rests = rest_recommand_memory[user_id]
    samples = rests.get_group(section_name).apply(get_group_sample)
    carousel = CarouselTemplate(columns=[
        create_rest_col(name, opentime, comment)
        for name, opentime, phone, section, addfress, comment in samples.values
    ])
    return TemplateMessage(
        type='template',
        altText="TemplateMessage",
        template=carousel
    )

@handler.add(PostbackEvent) 
def handle_postback(event):
    ts = event.postback.data
    postback_data ={k:v  for k,v in parse_qsl(ts)}
    response = postback_data.get('comment', "Get PostBack Event!") # 取得評價
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response)]
            )
        )

def handle_sample(user_message):
    if "按鈕sample" in user_message:
        return create_buttons_template()
    elif "輪播sample" in user_message:
        return create_carousel_template()
    elif "確認sample" in user_message:
        return create_check_template()
    else:
        return create_quick_reply()


if __name__ == "__main__":
    app.run(debug=True)