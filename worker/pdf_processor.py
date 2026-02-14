import fitz
from utils.language import detect_language
from utils.dictionary_builder import build_dictionary
from utils.pdf_export import export_dictionary_pdf

def process_pdf(pdf_path, chat_id=None, bot=None):
    doc = fitz.open(pdf_path)

    pages_text = []
    for page in doc:
        pages_text.append(page.get_text())

    full_text = " ".join(pages_text)
    language = detect_language(full_text)

    if bot:
        bot.send_message(chat_id, f"✅ زبان کتاب: {language}")

    dictionary = build_dictionary(pages_text, language)

    output_pdf = export_dictionary_pdf(dictionary)

    return output_pdf
