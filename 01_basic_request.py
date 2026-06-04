"""
Пример 1: Базовый запрос к Claude API.
Курс: Building with the Claude API -> "Подача запроса".

Что показывает:
- как создать клиент,
- как отправить одно сообщение,
- как достать текст ответа.
"""
import os
from dotenv import load_dotenv
import anthropic

# Загружаем ключ из файла .env в переменные окружения
load_dotenv()

# Клиент сам берёт ключ из переменной ANTHROPIC_API_KEY
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Минимум для запроса: модель, max_tokens, messages (это спрашивали в тесте!)
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    messages=[
        {"role": "user", "content": "Объясни простыми словами, что такое API. 2-3 предложения."}
    ],
)

# Ответ лежит в message.content[0].text
print(message.content[0].text)
