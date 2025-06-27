import re

class StringUtils:

    @staticmethod
    def normalize_text(text):
        if not isinstance(text, str):
            return ''

        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
        text = re.sub(r'_', '', text)
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    @staticmethod
    def replace_external_double_quotes(text):
        return re.sub(r'\["(.*)"\]', r"['\1']", text)
    
    @staticmethod
    def replace_external_single_quotes(text):
        return re.sub(r"\['(.*)'\]", r'["\1"]', text)
