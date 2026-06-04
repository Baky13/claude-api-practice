"""
Задача 3: показываем, КАК ломается хрупкий парсер (stop на '}'),
а потом чиним по-нормальному.
"""
import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Заставляем грейдер вставить символ } прямо в текст reasoning
GRADER_SYSTEM = (
    'Верни JSON вида {"score": число, "reasoning": "текст"}. '
    'В поле reasoning ОБЯЗАТЕЛЬНО упомяни закрывающую скобку "}" в кавычках.'
)
user_msg = "Оцени ответ 'Париж' на вопрос 'столица Франции'."

# ---------- ХРУПКИЙ способ: stop_sequences=['}'] ----------
print("=== ХРУПКИЙ способ (stop на первой '}') ===")
text = client.messages.create(
    model="claude-sonnet-4-6", max_tokens=200, system=GRADER_SYSTEM,
    messages=[{"role": "user", "content": user_msg}],
    stop_sequences=["}"],          # <-- остановится на ПЕРВОЙ } (внутри reasoning!)
).content[0].text
raw_fragile = "{" + text.split("{", 1)[-1] + "}"   # дописываем } как в исходном коде
print("Собранный JSON:", repr(raw_fragile))
try:
    print("Распарсили:", json.loads(raw_fragile))
except json.JSONDecodeError as e:
    print(f"❌ ПАДЕНИЕ: {e}  <- стоп оборвал JSON на скобке внутри текста")

# ---------- НАДЁЖНЫЙ способ: без stop, парсим весь валидный JSON ----------
print("\n=== НАДЁЖНЫЙ способ (без stop, парсим целиком) ===")
raw = client.messages.create(
    model="claude-sonnet-4-6", max_tokens=200,
    system="Верни ТОЛЬКО валидный JSON {\"score\": число, \"reasoning\": \"текст\"}, без текста вокруг.",
    messages=[{"role": "user", "content": user_msg}],
).content[0].text.strip()
if raw.startswith("```"):
    raw = raw.strip("`").lstrip("json").strip()
print("Ответ:", repr(raw))
print("Распарсили:", json.loads(raw))   # скобки внутри текста больше не проблема
# Ещё надёжнее: tool use со схемой (модель ОБЯЗАНА вернуть структуру).
