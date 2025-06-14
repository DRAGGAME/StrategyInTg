from openai import OpenAI

from config import API_NN, KEY_NN

import requests

# 🔐 Замените на ваш API-ключ DeepSeek
    x = '1'
# 🌐 URL API DeepSeek (если используется OpenAI-совместимый API)
print(x[1])

def chat_with_model(token, url):
    url = url
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
      "model": "qwen2.5-coder:32b",
      "messages": [
        {
          "role": "user",
          "content": "Как дела?"
        }
      ]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# # 📤 Вывод результата
data = chat_with_model(KEY_NN, API_NN)
reply = data["choices"][0]["message"]["content"]
print(reply[1])
