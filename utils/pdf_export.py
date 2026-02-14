from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import arabic_reshaper
from bidi.algorithm import get_display

def fa(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def export_dictionary_pdf(dictionary):
    file_name = "dictionary_output.pdf"
    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()
    story = []

    for section, words in dictionary.items():
        story.append(Paragraph(section, styles["Heading2"]))
        for w, t in words.items():
            story.append(Paragraph(f"{w} : {fa(t)}", styles["Normal"]))

    doc.build(story)
    return file_name
