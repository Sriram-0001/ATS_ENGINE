import re

class ExperienceExtractor:

    @staticmethod
    def extract(text: str):
        text = text.lower()

        # find patterns like "2 years", "3+ years"
        matches = re.findall(r'(\d+)\s*\+?\s*years?', text)

        if not matches:
            return 0

        years = [int(x) for x in matches]
        return max(years)