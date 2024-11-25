import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import TELEGRAM_TOKEN, GITHUB_TOKEN, GITHUB_API_URL
from handlers import start, process_callback



# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

dp.message.register(start, Command("start"))
dp.callback_query.register(process_callback, lambda c: True)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())