from openai import OpenAI

from config import DEEPSEEK_API_KEY

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)


async def ask_agent(message: str) -> str:
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": "Ты полезный ИИ-агент. Отвечай понятно, кратко и по делу."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content