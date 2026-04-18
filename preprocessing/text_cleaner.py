import re


class TextCleaner:

    @staticmethod
    def clean(text):
        text = text.lower()
        text = re.sub(r"\s+", " ", text)
        return text.strip()