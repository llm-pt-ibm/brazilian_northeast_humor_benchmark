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
    def has_list_structure(text: str) -> bool:
        """Verifica se o texto contém uma lista (mesmo que mal formatada)."""
        match = re.search(r"\[.*?\]", text, re.DOTALL)
        return bool(match)

    @staticmethod
    def has_no_quote_errors(text: str) -> bool:
        if re.search(r'""', text) or re.search(r"''", text):
            return False

        if re.search(r'\["([\'"]).*?\1"\]', text):
            return False
        if re.search(r"\['([\"']).*?\1'\]", text):
            return False

        return True

    @staticmethod
    def is_valid_list_of_strings(text: str) -> bool:
        # Primeiro: tem estrutura de lista?
        if not StringUtils.has_list_structure(text):
            return False

        # Segundo: não pode ter erros de aspas
        if not StringUtils.has_no_quote_errors(text):
            return False

        # Agora tenta avaliar o texto limpo
        try:
            val = ast.literal_eval(text)
            if isinstance(val, list) and all(isinstance(item, str) for item in val):
                return True
        except Exception:
            return False

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
        text = re.sub(r'""', '"', text) 
        text = re.sub(r"''", "'", text)

        text = re.sub(r'\["([\'"])(.*?)\1"\]', r'["\2"]', text)
        text = re.sub(r"\['([\"'])(.*?)\1'\]", r"['\2']", text)

        return text