import os
import asyncio
import threading
from fastapi import FastAPI
import uvicorn

from aiogram import Bot, Dispatcher
from handlers import router

# BOT_TOKEN ni environmentdan olamiz
API_TOKEN = os.getenv("BOT_TOKEN")

# ============================
# 🚀 FASTAPI HEALTH CHECK
# ============================
app = FastAPI()

@app.get("/")
def alive():
    return {"status": "ok"}

def start_web():
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

# ============================
# 🚀 AIROGRAM POLLING
# ============================
async def start_bot():
    if not API_TOKEN:
        raise RuntimeError("BOT_TOKEN set qilinmagan!")

    bot = Bot(API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

# ============================
# 🚀 MAIN
# ============================
if __name__ == "__main__":
    threading.Thread(target=start_web).start()
    asyncio.run(start_bot())
