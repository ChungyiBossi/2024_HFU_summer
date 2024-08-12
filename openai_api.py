from openai import OpenAI
import os
from pprint import pprint


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

chat_history = dict()

def chat_with_chatgpt(user_id, user_message, openai_api_key):
    # 利用OpenAI類別，建立一個可以跟OpenAI伺服器互動的物件
    client = OpenAI(api_key=openai_api_key)

    # 把使用者的訊息，加對話紀錄裡
    if user_id in chat_history:
        chat_history[user_id].append({"role": "user", "content": user_message})
    else:
        chat_history[user_id] = [{"role": "user", "content": user_message}]
    message = user_message + '  請用條列式的方式回答。' # 加料
    
    # 完成一段對話
    chat_completion = client.chat.completions.create(
        messages=chat_history[user_id][:-1] + [{"role": "user", "content": message}],
        model="gpt-3.5-turbo",
    )

    response = chat_completion.choices[0].message.content

    # 把ChatGPT的訊息，加對話紀錄裡
    chat_history[user_id].append({"role": "system", "content": response})
    return response if response else "No Content."

if __name__ == '__main__':
    api_key = os.getenv("OPENAI_API_KEY", None)

    while True:
        user_message = input("請輸入一句話，跟ChatGPT聊天 :")
        if user_message == 'quit':
            print("對話結束。")
            break

        if api_key and user_message:
            response = chat_with_chatgpt(user_message, api_key)
            print("ChatGPT say:", response)
        else:
            print("api key not found: ", api_key)
        
        print("History: ")
        pprint(chat_history)
        print()