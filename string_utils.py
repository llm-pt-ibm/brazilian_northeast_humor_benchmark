import re
import ast

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
    def extract_binary_digit(value: str) -> str | None:
        match = re.search(r'\b[01]\b', value.strip())
        if match:
            return match.group(0)
        return None

    @staticmethod
    def extract_list_of_strings_from_text(text: str) -> list[str]:
        match = re.search(r"\[.*?\]", text, re.DOTALL)
        if not match:
            return []

        list_str = match.group()

        cleaned_str = StringUtils.clean_quoted_string_list(list_str)

        try:
            strings_list = ast.literal_eval(cleaned_str)
            if isinstance(strings_list, list) and all(isinstance(item, str) for item in strings_list):
                return strings_list
        except Exception:
            pass

        return []

    @staticmethod
    def clean_quoted_string_list(text: str) -> str:
        # Corrige ["texto"] que veio com aspas duplicadas: ["texto""]
        # Substitui aspas duplicadas internas por aspas simples, com cuidado
        text = re.sub(r'""', '"', text)  # corrige aspas duplas duplicadas internas
        text = re.sub(r"''", "'", text)

        # Remove aspas externas duplicadas: ["'texto'"] -> ["texto"]
        text = re.sub(r'\["([\'"])(.*?)\1"\]', r'["\2"]', text)
        text = re.sub(r"\['([\"'])(.*?)\1'\]", r"['\2']", text)

        return text