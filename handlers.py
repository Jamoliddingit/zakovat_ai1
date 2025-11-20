from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram import F
import httpx

from utils import user_states, init_user, is_similar

router = Router()

# API URL NI STRING QILIB QO'YAMIZ
API_URL = "https://zakovat-ai.onrender.com"


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    init_user(user_id)

    await message.answer(
        f"Assalomu alaykum, *{message.from_user.full_name}*! 👋\n"
        "Bu — *Zakovat PRO*.\n"
        "Savol olish: /play\n"
        "Statistika: /stats",
        parse_mode=ParseMode.MARKDOWN
    )


@router.message(Command("stats"))
async def stats_cmd(message: types.Message):
    user_id = message.from_user.id
    init_user(user_id)
    d = user_states[user_id]

    acc = round(d["correct"] / d["asked"] * 100, 1) if d["asked"] else 0

    await message.answer(
        f"📊 *Statistika*\n\n"
        f"Savollar: {d['asked']}\n"
        f"To‘g‘ri: {d['correct']}\n"
        f"Aniqlik: {acc}%",
        parse_mode=ParseMode.MARKDOWN
    )


@router.message(Command("play"))
async def play_cmd(message: types.Message):
    user_id = message.from_user.id
    init_user(user_id)

    async with httpx.AsyncClient() as client:
        res = await client.get(f"{API_URL}/questions/random")

    try:
        q = res.json()
    except Exception:
        return await message.answer("❌ API error.")

    if "error" in q:
        return await message.answer("❌ Savollar mavjud emas.")

    if "id" not in q or "question" not in q:
        return await message.answer(f"❌ API noto‘g‘ri format:\n{q}")

    user_states[user_id]["current"] = q["id"]
    user_states[user_id]["asked"] += 1

    await message.answer(
        f"🧠 *Savol:*\n\n{q['question']}\n\n_Javobni yozing..._",
        parse_mode=ParseMode.MARKDOWN
    )


@router.message(F.text)
async def answer_handler(message: types.Message):
    user_id = message.from_user.id
    init_user(user_id)

    cid = user_states[user_id]["current"]
    if cid == 0:
        return await message.answer("Avval /play bosing 🙂")

    async with httpx.AsyncClient() as client:
        res = await client.get(f"{API_URL}/questions/{cid}")
        q = res.json()

    correct = q["answer"]
    explain = q["explanation"]

    if is_similar(message.text, correct):
        result = "✅ *To‘g‘ri!*"
        user_states[user_id]["correct"] += 1
    else:
        result = "❌ *Noto‘g‘ri.*"

    user_states[user_id]["current"] = 0

    await message.answer(
        f"{result}\n\nTo‘g‘ri javob: _{correct}_\n"
        f"Izoh: _{explain}_\n\n/play — Keyingi savol",
        parse_mode=ParseMode.MARKDOWN
    )
