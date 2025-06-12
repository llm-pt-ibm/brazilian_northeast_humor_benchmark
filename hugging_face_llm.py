from transformers import pipeline
from huggingface_hub import login

class HuggingFaceLLM:
    def __init__(self, model_name, task="text-generation", device=-1, token=None):
        print(token)
        if token:
            login(token=token)

        self.pipeline = pipeline(
            task=task,
            model=model_name,
            device=device,
            token=token
        )

    def generate(self, prompt, **kwargs):
        return self.pipeline(prompt, **kwargs)[0]['generated_text']