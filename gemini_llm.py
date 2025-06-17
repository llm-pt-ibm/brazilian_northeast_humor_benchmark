from google import genai

class GeminiLLM:
    def __init__(self, api_key: str, model_name):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            **kwargs
        )
        return response.text
