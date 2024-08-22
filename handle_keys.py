import os, sys

def get_secret_and_token():
    # 1. 先到Line Developer Console，把 Channel Secret & Channel Access Token複製起來
    # 2. 把這兩個密文，存到環境變數內；工具列搜尋<環境變數>，新增兩個環境變數，並且把值貼上去
    # 3. 按下確定儲存，要記得你的變數名稱，這些資訊只會存在你當前使用的電腦裡。
    # 4. 透過以下程式碼，取得環境變數儲存的對應數值。

    tokens_name = [
        'LINEBOT_SECRET_KEY',
        'LINEBOT_ACCESS_TOKEN',
        "OPENAI_API_KEY",
        "CWA_API_KEY",
        "IMGUR_CLIENT_ID",
        "IMGUR_SECRET_KEY"
    ]

    keys = dict()
    for token_name in tokens_name:
        token = os.getenv(token_name, None)
        if token is None:
            print(f'Specify {token_name} as environment variable.')
            sys.exit(1)
        keys[token_name] = token

    return keys