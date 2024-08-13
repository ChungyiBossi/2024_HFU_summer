# OpenAI ChatGPT Chat Completition
### Goal - 透過ChatGPT生成通順的回覆，我們可以依照prompt去調整內容

1. 前往ChatGPT Platform，取得API Key
2. 把授權碼存到本機的環境變數
3. 使用他的官方範例，可以從[github](https://github.com/openai/openai-python)找到
    * OpenAI 提供與ChatGPT溝通的python API
    * 此API可以給歷史訊息，但會需要由使用方提供
    * 有分: user/system，分別代表使用者跟ChatGPT
4. 串接Linebot，用Linebot user_id 管理對話歷史紀錄
    ```python
    {
        'user_id_a': [
            {'role': 'user', 'content': 'xxx'},
            {'role': 'system', 'content': 'yyy'},
            {'role': 'user', 'content': 'xxx'},
            {'role': 'system', 'content': 'yyy'},
        ],
        'user_id_b': [
            {'role': 'user', 'content': 'aaa'},
            {'role': 'system', 'content': 'bbb'},
            {'role': 'user', 'content': 'ccc'},
            {'role': 'system', 'content': 'ddd'},
        ]
    }
    ```
5. 串接到Linebot