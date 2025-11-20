import asyncio
import os
from aiogram import Bot, Dispatcher
from handlers import router

# BOT_TOKEN ni environmentdan olamiz
API_TOKEN = os.getenv("8491503418:AAGjLVXXGlglXQjo7zHXPzzAqW0z0WPXSow")


async def main():
    if not API_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable set qilinmagan. Render yoki Railway’da env ga qo‘sh.")

    bot = Bot(API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
