"""
Пример 7: Использование инструментов (tool use).
Курс: "Использование инструментов с Claude".

Главная идея: Claude НЕ выполняет функцию сам.
Он говорит "вызови инструмент X с такими аргументами" -> ВЫПОЛНЯЕТ наш код ->
мы возвращаем результат -> Claude формулирует финальный ответ.
"""
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


# 1. Наша настоящая функция (её выполняет программа, не Claude)
def get_weather(city: str) -> str:
    fake_db = {"Бишкек": "+28°C, ясно", "Москва": "+15°C, дождь"}
    return fake_db.get(city, "нет данных")


# 2. Описание инструмента для Claude (схема)
tools = [
    {
        "name": "get_weather",
        "description": "Возвращает текущую погоду в указанном городе",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "Название города"}},
            "required": ["city"],
        },
    }
]

messages = [{"role": "user", "content": "Какая погода в Бишкеке?"}]

# 3. Первый запрос — Claude решает вызвать инструмент
resp = client.messages.create(
    model="claude-sonnet-4-6", max_tokens=400, tools=tools, messages=messages
)

# 4. Если Claude попросил инструмент — выполняем его НАШИМ кодом
if resp.stop_reason == "tool_use":
    tool_call = next(b for b in resp.content if b.type == "tool_use")
    result = get_weather(tool_call.input["city"])   # <-- выполняет программа
    print(f"[Claude попросил get_weather('{tool_call.input['city']}') -> {result}]")

    # 5. Возвращаем результат Claude и получаем финальный ответ
    messages.append({"role": "assistant", "content": resp.content})
    messages.append({
        "role": "user",
        "content": [{
            "type": "tool_result",
            "tool_use_id": tool_call.id,
            "content": result,
        }],
    })
    final = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=400, tools=tools, messages=messages
    )
    print(final.content[0].text)
