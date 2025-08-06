from openai import OpenAI

class OpenAiLLM:
    def __init__(self, api_key: str, model_name: str, base_url: str = "https://api.openai.com/v1"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_name = model_name

    def generate(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content