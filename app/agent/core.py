import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.tools.weather import get_weather
from app.tools.web_search import search_web
from app.tools.calculator import calc

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Ищет актуальную информацию в интернете",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Поисковый запрос",
                    }
                },
                "required": ["query"],
            },
        },
    },
        {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Вычисляет математическое выражение",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Математическое выражение",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "weather",
            "description": "Получает текущую погоду в указанном городе",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Название города, например Moscow, Tokyo",
                    }
                },
                "required": ["city"],
            },
        },
    }
]


available_tools = {
    "search_web": search_web,
    "calculator": calc,
    "weather": get_weather
}


async def ask_agent(user_message: str) -> str:
    messages = [
        {
            "role": "system",
            "content": """
Ты ИИ-агент с доступом к интернету, и ты отвечаешь пользователю внутри Telegram-бота.


Правила:
1. Если вопрос требует актуальной информации — используй search_web.
2. Если вопрос про новости, цены, версии библиотек, вакансии, погоду, компании, события — используй search_web.
3. Если вопрос можно решить без интернета — отвечай сам.
4. Не выдумывай факты. Если использовал интернет, опирайся на найденные данные.
5. Если пользователь написал математическое выражение - используй calculator
6. Если пользователь просит узнать прогноз погоды - используй weather

Формат ответа:
- Не используй Markdown.
- Не используй **жирный текст**, `код`, заголовки #, таблицы и списки со сложной разметкой.
- Пиши красиво, но обычным текстом.
- Можно использовать эмодзи, короткие абзацы и простые списки через дефис.
- Ответ должен быть готов к отправке в Telegram без дополнительной обработки.

""",  # noqa: RUF001
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    first_response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    message = first_response.choices[0].message

    if not message.tool_calls:
        return message.content

    messages.append(message)

    for tool_call in message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        tool_result = available_tools[function_name](**arguments)

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(tool_result),
            }
        )

    second_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
    )

    return second_response.choices[0].message.content

