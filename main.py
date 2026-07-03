import asyncio

from app.services.logger import log
from app.telegram.bot.bot import bot, dp


async def main():
    try:
        await dp.start_polling(bot, timeout=60)
        log.info("Бот запущен")
    except Exception as e:  # noqa: BLE001
        log.exception("Бот не запущен, ошибка: ",e)



if __name__ == "__main__":
    asyncio.run(main())

