
# Line Bot SDK Message Samples
from linebot.v3.messaging import ( # 傳輸回Line官方後台的資料格式
    TextMessage, ImageMessage, StickerMessage,
    TemplateMessage, 
    ButtonsTemplate, CarouselTemplate, CarouselColumn, ConfirmTemplate,
    PostbackAction, MessageAction, LocationAction, CameraAction, CameraRollAction, URIAction,
    QuickReply, QuickReplyItem
)


def create_sticker_message():
    # https://developers.line.biz/en/docs/messaging-api/sticker-list/#send-sticker
    return StickerMessage(
        packageId=446,
        stickerId=1988,
        # quoteToken="message quote token"
    )


def create_image_message(original_link, preview_link):
    return ImageMessage(
        originalContentUrl=original_link,
        previewImageUrl=preview_link
    )

def create_text_message(display_text, quick_reply_items=[]):
    # https://developers.line.biz/en/reference/messaging-api/#text-message
    if quick_reply_items:
        return TextMessage(text=display_text, quickReply=quick_reply_items)
    else:
        return TextMessage(text=display_text)

def create_buttons_template():
    response = ButtonsTemplate(
        title='Menu',
        text='Please select',
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
        QuickReplyItem(action=MessageAction(label='按鈕sample', text='按鈕sample')),
        QuickReplyItem(action=MessageAction(label='輪播sample', text='輪播sample')),
        QuickReplyItem(action=MessageAction(label='確認sample', text='確認sample')),
        QuickReplyItem(action=MessageAction(label='快速回覆sample', text='快速回覆sample')),
        QuickReplyItem(action=LocationAction(label='我在...', text='Location')),
        QuickReplyItem(action=CameraAction(label='打開相機', text='Camera')),
        QuickReplyItem(action=CameraRollAction(label='打開相簿', text='Photos')),
        QuickReplyItem(action=URIAction(label='前往GOOGLE', uri='https://www.google.com')),
        QuickReplyItem(action=PostbackAction(label='預約', data='key1=value2&key2=value2'))
    ])

    return TextMessage(
        text="超快速回覆",
        quickReply=quick_reply_body
    )