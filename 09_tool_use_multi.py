"""
Задача 1: ДВА инструмента — Claude сам выбирает нужный.
Бонус: чиним проблему next() — обрабатываем ВСЕ блоки tool_use, а не только первый.
"""
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


# --- Две настоящие функции ---
def get_weather(city: str) -> str:
    return {"Бишкек": "+28°C, ясно", "Москва": "+15°C, дождь"}.get(city, "нет данных")


def get_time(city: str) -> str:
    return {"Бишкек": "14:00", "Москва": "11:00"}.get(city, "нет данных")


# Реестр: имя инструмента -> функция (чтобы вызвать по имени, которое назвал Claude)
TOOL_FUNCS = {"get_weather": get_weather, "get_time": get_time}

# Описания ОБОИХ инструментов для Claude
tools = [
    {
        "name": "get_weather",
        "description": "Возвращает погоду в городе",
        "input_schema": {"type": "object",
            "properties": {"city": {"type": "string"}}, "required": ["city"]},
    },
    {
        "name": "get_time",
        "description": "Возвращает текущее время в городе",
        "input_schema": {"type": "object",
            "properties": {"city": {"type": "string"}}, "required": ["city"]},
    },
]

# Вопрос про ВРЕМЯ -> Claude должен сам выбрать get_time, а не get_weather
messages = [{"role": "user", "content": "Который сейчас час в Москве?"}]

resp = client.messages.create(
    model="claude-sonnet-4-6", max_tokens=400, tools=tools, messages=messages
)

if resp.stop_reason == "tool_use":
    messages.append({"role": "assistant", "content": resp.content})  # сохраняем просьбу Claude

    tool_results = []
    # ВАЖНО: цикл по ВСЕМ блокам tool_use (а не next() — иначе потеряли бы второй)
    for block in resp.content:
        if block.type == "tool_use":
            func = TOOL_FUNCS[block.name]   # выбираем функцию по имени, что назвал Claude
            result = func(**block.input)    # вызываем с его аргументами
            print(f"[Claude выбрал {block.name}({block.input}) -> {result}]")
            tool_results.append({
                "type": "tool_result", "tool_use_id": block.id, "content": result,
            })

    messages.append({"role": "user", "content": tool_results})
    final = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=400, tools=tools, messages=messages
    )
    print(final.content[0].text)
