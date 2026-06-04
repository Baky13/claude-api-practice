"""
Пример 8: Оценка промптов (prompt evaluation) с модельным грейдером.
Курс: "Оперативная оценка".

Идея: не угадывать "хороший ли промпт", а ИЗМЕРИТЬ.
1) тестовые вопросы -> 2) прогоняем промпт -> 3) ГРЕЙДЕР оценивает ответы.
Грейдеры: код / человек / модельный (другой ИИ). Здесь — модельный.
"""
import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Промпт, который мы тестируем
SYSTEM = "Ты помощник. Отвечай ОДНИМ словом, без объяснений."

# Тестовый набор: вопрос + что ожидаем
test_cases = [
    {"q": "Столица Франции?", "expected": "Париж"},
    {"q": "2+2?", "expected": "4"},
]

for case in test_cases:
    # шаг 1-2: получаем ответ от тестируемого промпта
    answer = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=50,
        system=SYSTEM,
        messages=[{"role": "user", "content": case["q"]}],
    ).content[0].text.strip()

    # шаг 3: МОДЕЛЬНЫЙ грейдер — просим другой вызов оценить + объяснить рассуждение
    grade_raw = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=200,
        system="Ты строгий проверяющий. Верни JSON: {\"score\": 0-10, \"reasoning\": \"...\"}.",
        messages=[{"role": "user", "content":
            f"Вопрос: {case['q']}\nОжидалось: {case['expected']}\nОтвет: {answer}\nОцени."}],
        stop_sequences=["}"],
    ).content[0].text
    grade = json.loads("{" + grade_raw.split("{", 1)[-1] + "}")

    print(f"Q: {case['q']:20} A: {answer:10} -> score={grade['score']} ({grade['reasoning']})")
