import re
from collections import defaultdict
import requests

# استخراج لغات از متن
def extract_words(text):
    # فقط حروف و اعداد لاتین
    words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", text)
    return words

# ترجمه رایگان با LibreTranslate
def translate_word(word, target_lang="fa"):
    url = "https://libretranslate.com/translate"
    payload = {
        "q": word,
        "source": "en",
        "target": target_lang,
        "format": "text"
    }
    try:
        r = requests.post(url, data=payload, timeout=10)
        if r.status_code == 200:
            return r.json().get("translatedText", word)
        else:
            return word
    except Exception as e:
        print("Translation error:", e)
        return word

# ساخت دیکشنری برای هر 5 صفحه
def build_dictionary(pages_text, lang):

    result = defaultdict(dict)
    chunk_size = 5

    for i in range(0, len(pages_text), chunk_size):
        chunk = pages_text[i:i+chunk_size]
        chunk_text = " ".join(chunk)

        words = extract_words(chunk_text)
        unique_words = sorted(set(words))

        page_key = f"Pages {i+1}-{i+len(chunk)}"

        for w in unique_words:
            result[page_key][w] = translate_word(w)

    return result
