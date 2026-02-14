import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from worker.tasks import process_pdf_task
import os

BOT_TOKEN = os.getenv('bottoken')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "سلام 👋\n"
        "PDF کتاب زبان اصلی خود را ارسال کنید."
    )


@dp.message(lambda m: m.document and m.document.file_name.endswith(".pdf"))
async def handle_pdf(message: types.Message):
    await message.answer("✅ فایل دریافت شد")

    file_info = await bot.get_file(message.document.file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"

    await message.answer("🔍 در حال تشخیص زبان و آماده‌سازی پردازش...")

    process_pdf_task.delay(file_url, message.chat.id)

    await message.answer(
        "⚙️ پردازش شروع شد.\n"
        "⏳ زمان تقریبی: چند دقیقه بسته به حجم کتاب"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
