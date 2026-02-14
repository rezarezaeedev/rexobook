import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# -------------------------
# Logging
# -------------------------
logging.basicConfig(level=logging.INFO)

# -------------------------
# Environment Variables
# -------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
PORT = int(os.getenv("PORT", 10000))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")
if not RENDER_EXTERNAL_URL:
    raise ValueError("RENDER_EXTERNAL_URL environment variable is not set!")

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}{WEBHOOK_PATH}"

# -------------------------
# Bot & Dispatcher
# -------------------------
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# -------------------------
# Handlers
# -------------------------
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "سلام 👋\n\n"
        "ربات با موفقیت روی Render (Webhook) اجرا شد."
    )

@dp.message()
async def echo_handler(message: types.Message):
    await message.answer("پیام دریافت شد ✅")

# -------------------------
# Webhook Setup
# -------------------------
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set to {WEBHOOK_URL}")

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    await bot.session.close()
    logging.info("Bot shutdown")

# -------------------------
# Main
# -------------------------
def main():
    app = web.Application()

    # ثبت dispatcher
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    logging.info("Starting bot...")
    web.run_app(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
