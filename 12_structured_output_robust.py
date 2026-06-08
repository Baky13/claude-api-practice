"""
НАДЁЖНЫЙ структурированный вывод (ответ на замечание: "верни JSON" в промпте — ненадёжно).

Правильно — задавать СХЕМУ, тогда модель ОБЯЗАНА вернуть структуру.
Два рабочих способа (оба проверены запуском):
  Способ 1 — Structured Outputs (output_config + json_schema)  ← новый, самый чистый
  Способ 2 — Tool use со схемой (input_schema + tool_choice)   ← классический
"""
import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Схема нужной структуры. ВАЖНО: для object нужен "additionalProperties": False
schema = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "name": {"type": "string"},
        "price": {"type": "number"},
        "in_stock": {"type": "boolean"},
    },
    "required": ["name", "price", "in_stock"],
}

prompt = "Придумай реалистичные данные о товаре 'кроссовки' (название, цена, в наличии)."

# ---------- Способ 1: Structured Outputs ----------
print("=== Способ 1: Structured Outputs (output_config) ===")
msg = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    output_config={"format": {"type": "json_schema", "schema": schema}},  # задаём форму ответа
    messages=[{"role": "user", "content": prompt}],
)
data = json.loads(msg.content[0].text)   # гарантированно валидный JSON по схеме
print("Структура:", data, "| цена:", data["price"])

# ---------- Способ 2: Tool use со схемой ----------
print("\n=== Способ 2: Tool use (input_schema + tool_choice) ===")
tools = [{"name": "save_product", "description": "Сохраняет данные о товаре", "input_schema": schema}]
msg2 = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    tools=tools,
    tool_choice={"type": "tool", "name": "save_product"},  # ЗАСТАВЛЯЕМ вызвать инструмент
    messages=[{"role": "user", "content": prompt}],
)
tool_call = next(b for b in msg2.content if b.type == "tool_use")
data2 = tool_call.input   # уже готовый dict, парсить не надо
print("Структура:", data2, "| цена:", data2["price"])

# Вывод: в обоих случаях модель ОБЯЗАНА вернуть структуру по схеме —
# в отличие от "попроси JSON в промпте", где она может добавить текст и сломать парсер.
