import asyncio
import logging
from aiogram import Dispatcher, Bot
from app.handlers import router  # Импортируем роутер из handlers
from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)  # Подключаем роутер к диспетчеру
    logging.basicConfig(level=logging.INFO)

    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем возможные старые обновления
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
