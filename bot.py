import json
import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import (
    BOT_TOKEN, ADMIN_CHAT_ID,
    STRIPE_LINK_49, STRIPE_LINK_199, STRIPE_LINK_399,
    ACCESS_49, ACCESS_199, ACCESS_399
)

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    parts = m.text.split()
    users = load_users()
    uid = str(m.from_user.id)

    if len(parts) == 2:
        access_token = parts[1]
        if access_token in [ACCESS_49, ACCESS_199, ACCESS_399]:
            if uid not in users:
                users[uid] = access_token
                save_users(users)
            await m.answer("✅ DOSTĘP AKTYWOWANY! Możesz teraz korzystać z funkcji bota.")
            return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 Pakiet START – 49 zł", callback_data="show_49")],
        [InlineKeyboardButton(text="💼 Pakiet SMART – 199 zł (PROMO)", callback_data="show_199")],
        [InlineKeyboardButton(text="🚀 Pakiet PRO – 399 zł", callback_data="show_399")],
        [InlineKeyboardButton(text="ℹ️ O bocie", callback_data="show_info")]
    ])
    await m.answer(
        "👋 Cześć! Wybierz jeden z pakietów, aby aktywować dostęp do bota:",
        reply_markup=kb
    )

@dp.callback_query(lambda c: c.data.startswith("show_"))
async def show_package_info(cq: types.CallbackQuery):
    data = cq.data

    if data == "show_49":
        text = (
            "*📦 Pakiet START – 49 zł*\n"
            "- Podstawowy bot w Telegramie\n"
            "- Formularz zapisu (Google Sheet)\n"
            "- Prosta konfiguracja + pomoc\n\n"
            "👉 Po płatności napisz `/start access49`"
        )
        url = STRIPE_LINK_49

    elif data == "show_199":
        text = (
            "*💼 Pakiet SMART – 199 zł (PROMO)*\n"
            "- Bot do zapisu wizyt (Telegram)\n"
            "- Połączenie z arkuszem Google\n"
            "- Odpowiada na pytania klientów\n"
            "- Szybkie wdrożenie, pomoc techniczna\n\n"
            "👉 Po płatności napisz `/start access199`"
        )
        url = STRIPE_LINK_199

    elif data == "show_399":
        text = (
            "*🚀 Pakiet PRO – 399 zł*\n"
            "- Wszystko z pakietu SMART\n"
            "- + Automatyczne przypomnienia\n"
            "- + Obsługa wielu terminów\n"
            "- + Personalizacja i rozbudowa\n\n"
            "👉 Po płatności napisz `/start access399`"
        )
        url = STRIPE_LINK_399

    else:
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Zapłać teraz", url=url)]
    ])
    await bot.send_message(cq.from_user.id, text, reply_markup=kb)
    await cq.answer()

@dp.callback_query(lambda c: c.data == "show_info")
async def show_bot_info(cq: types.CallbackQuery):
    print(f"Callback data: {cq.data} (show_info pressed)")
    text = (
        "*🤖 Czym jest ten bot?*\n\n"
        "To prosty asystent, który pomaga:\n"
        "✅ Automatycznie odpowiada klientom\n"
        "✅ Zapisuje dane do Google Sheet\n"
        "✅ Oszczędza Twój czas i działa 24/7\n\n"
        "Ten bot powstał z myślą o małych firmach, które chcą automatyzować kontakt z klientem 📲"
    )
    await cq.message.answer(text, parse_mode=ParseMode.MARKDOWN)
    await cq.answer()

async def main():
    print("✅ Bot uruchomiony.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
