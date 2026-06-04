"""
Задача 2: AGENT LOOP — несколько раундов tool_use, пока Claude не закончит.
Вопрос требует ДВУХ вызовов (погода двух городов), поэтому одного прохода мало.
"""
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def get_weather(city: str) -> str:
    return {"Бишкек": "+28°C, ясно", "Москва": "+15°C, дождь"}.get(city, "нет данных")


TOOL_FUNCS = {"get_weather": get_weather}
tools = [{
    "name": "get_weather",
    "description": "Возвращает погоду в городе",
    "input_schema": {"type": "object",
        "properties": {"city": {"type": "string"}}, "required": ["city"]},
}]

messages = [{"role": "user", "content": "Сравни погоду в Бишкеке и Москве — где теплее?"}]

# === AGENT LOOP ===
# Крутимся, ПОКА Claude просит инструменты. Выходим, когда дал финальный ответ.
while True:
    resp = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=500, tools=tools, messages=messages
    )

    if resp.stop_reason != "tool_use":
        # Claude перестал просить инструменты -> это финальный ответ
        print("\nФИНАЛ:", resp.content[0].text)
        break

    # Иначе — выполняем все запрошенные инструменты и возвращаем результаты
    messages.append({"role": "assistant", "content": resp.content})
    tool_results = []
    for block in resp.content:
        if block.type == "tool_use":
            result = TOOL_FUNCS[block.name](**block.input)
            print(f"[раунд: {block.name}({block.input}) -> {result}]")
            tool_results.append({
                "type": "tool_result", "tool_use_id": block.id, "content": result,
            })
    messages.append({"role": "user", "content": tool_results})
    # ...и цикл повторяется: снова зовём Claude
