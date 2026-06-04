"""
Пример 5: Потоковый вывод (streaming).
Курс: "Потоковая трансляция в ответах".

Streaming = ответ приходит по кусочкам (как печатается в чате),
а не целиком в конце. Удобно для интерфейсов — пользователь видит ответ сразу.
"""
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# client.messages.stream(...) вместо create(...)
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=300,
    messages=[{"role": "user", "content": "Расскажи короткий факт о космосе."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)  # печатаем по мере поступления
print()  # перенос строки в конце
