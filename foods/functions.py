from googletrans import Translator


def translate_to_english(korean_text):
    translator = Translator()
    translation = translator.translate(korean_text, src='ko', dest='en')
    english_text = translation.text
    return english_text


def translate_to_korea(english_text):
    translator = Translator()
    translation = translator.translate(english_text, src='en', dest='ko')
    korean_text = translation.text
    return korean_text

