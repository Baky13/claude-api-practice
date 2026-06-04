"""
Пример 2: Многоходовой диалог (multi-turn).
Курс: "Многоповоротные разговоры".

Главная идея: Claude САМ не помнит прошлые сообщения.
Память = ты передаёшь всю историю в списке messages.
"""
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Вся история диалога. Claude "помнит" только то, что здесь.
messages = [
    {"role": "user", "content": "Меня зовут Баки."},
    {"role": "assistant", "content": "Приятно познакомиться, Баки!"},
    {"role": "user", "content": "Как меня зовут?"},  # ответит верно ТОЛЬКО потому, что имя выше
]

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=200,
    messages=messages,
)

print(message.content[0].text)
# Если убрать первые два сообщения — Claude не будет знать имя. В этом весь смысл.
