from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from app.agent import ask_agent
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Привет! Я твой ИИ-агент. Напиши задачу.")


@dp.message()
async def message_handler(message: types.Message):
    answer = await ask_agent(message.text)

    await message.answer(answer)
