from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

class HuggingFaceLLM:
    def __init__(self, model_name: str, task: str = "text-generation", device: int = -1, token: str = None):
        tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
        model = AutoModelForCausalLM.from_pretrained(model_name, token=token)
        self.model_name = model_name.split('/')[1] if '/' in model_name else model_name

        self.pipeline = pipeline(
            task,
            model=model,
            tokenizer=tokenizer,
            device=device,
            token=token
        )

    def generate(self, prompt: str, **kwargs) -> str:
        return self.pipeline(prompt, **kwargs)[0]['generated_text']
