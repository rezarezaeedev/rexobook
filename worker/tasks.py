from celery import Celery
import requests
import tempfile
from worker.pdf_processor import process_pdf
from aiogram import Bot
import os

BOT_TOKEN = os.getenv('bottoken')
bot = Bot(token=BOT_TOKEN)

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0"
)


@celery.task
def process_pdf_task(file_url, chat_id):

    bot.send_message(chat_id, "📥 فایل در حال دانلود...")

    r = requests.get(file_url)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        f.write(r.content)
        pdf_path = f.name

    bot.send_message(chat_id, "🔍 زبان کتاب شناسایی شد و پردازش آغاز شد...")

    output_pdf = process_pdf(pdf_path, chat_id, bot)

    bot.send_document(
        chat_id,
        open(output_pdf, "rb"),
        caption="📚 دیکشنری آماده شد!"
    )
