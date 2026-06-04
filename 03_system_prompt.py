"""
Пример 3: Системный промпт (system prompt).
Курс: "Системные запросы".

System prompt задаёт РОЛЬ и поведение Claude, отдельно от самого диалога.
"""
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    # system — это и есть Description из AI Fluency: задаём контекст/стиль
    system="Ты опытный Python-разработчик. Отвечай кратко, с примером кода. Без воды.",
    messages=[
        {"role": "user", "content": "Как перевернуть строку?"}
    ],
)

print(message.content[0].text)
