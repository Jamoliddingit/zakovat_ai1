import os
import asyncio
import threading
from fastapi import FastAPI
import uvicorn
from fastapi.responses import JSONResponse

from aiogram import Bot, Dispatcher
from handlers import router

# BOT_TOKEN ni environmentdan olamiz
API_TOKEN = os.getenv("BOT_TOKEN")

# ============================
# 🚀 FASTAPI HEALTH CHECK (Render + UptimeRobot uchun)
# ============================
app = FastAPI()

# GET /
@app.get("/")
def alive():
    return {"status": "ok", "ping": True}

# HEAD /
@app.head("/")
def alive_head():
    return JSONResponse(content={"status": "ok"}, status_code=200)

# Qo‘shimcha/ping
@app.get("/ping")
def ping():
    return {"pong": True}


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
    # FastAPI alohida thread’da ishlaydi
    threading.Thread(target=start_web, daemon=True).start()

    # Aiogram polling asosiy loop’da
    asyncio.run(start_bot())
