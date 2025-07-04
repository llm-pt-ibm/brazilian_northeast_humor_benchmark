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
    def extract_list_of_strings_from_text(text: str) -> list[str]:
        match = re.search(r"\[.*?\]", text, re.DOTALL)
        list_str = match.group()

        formatted_strings_list = StringUtils().replace_external_double_quotes(list_str)
        try:
            strings_list = ast.literal_eval(list_str)
        except SyntaxError:
            formatted_strings_list = StringUtils().replace_external_single_quotes(list_str)
            strings_list = ast.literal_eval(formatted_strings_list)

        return strings_list
        
    @staticmethod
    def replace_external_double_quotes(text):
        return re.sub(r'\["(.*)"\]', r"['\1']", text)
    
    @staticmethod
    def replace_external_single_quotes(text):
        return re.sub(r"\['(.*)'\]", r'["\1"]', text)