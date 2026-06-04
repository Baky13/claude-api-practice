"""
Пример 6: Структурированный вывод (чистый JSON).
Курс: "Структурированные данные".

Задача: получить от Claude валидный JSON, который код сможет распарсить.
Способ: строгий system-промпт ("верни ТОЛЬКО JSON") + json.loads().

Примечание: есть и приём "prefill + stop_sequences" (начать ответ за Claude
символом "{"), но не все модели его поддерживают, поэтому здесь — надёжный вариант.
"""
import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    system="Ты возвращаешь ТОЛЬКО валидный JSON, без markdown-разметки и без пояснений.",
    messages=[
        {"role": "user", "content": "Дай данные о товаре 'кроссовки': поля name, price, in_stock."}
    ],
)

raw = message.content[0].text.strip()

# На всякий случай убираем ```json ... ``` если модель обернула в код-блок
if raw.startswith("```"):
    raw = raw.strip("`")
    raw = raw[raw.find("{"): raw.rfind("}") + 1]

print("Ответ:", raw)

data = json.loads(raw)   # парсим в словарь Python
print("Распарсили:", data)
print("Цена:", data["price"])
