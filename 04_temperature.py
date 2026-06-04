"""
Пример 4: Температура (temperature).
Курс: "Температура".

temperature = насколько ответ "креативный/случайный".
  0.0 -> строгий, предсказуемый (факты, код)
  1.0 -> креативный, разнообразный (тексты, идеи)
"""
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

prompt = "Придумай название для кофейни одним словом."

for temp in (0.0, 1.0):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=50,
        temperature=temp,        # <-- меняем температуру
        messages=[{"role": "user", "content": prompt}],
    )
    print(f"temperature={temp}: {message.content[0].text}")

# При 0.0 ответ почти всегда одинаковый; при 1.0 — разный каждый запуск.
