from hugging_face_llm import HuggingFaceLLM
from api_llm import ApiLLM

class LLMFactory:
    @staticmethod
    def create_llm(config: dict):
        provider = config.get("provider")

        if provider == "huggingface":
            return HuggingFaceLLM(
                model_name=config["model_name"],
                task=config.get("task", "text-generation"),
                device=config.get("device", -1),
                token=config['token']
            )

        elif provider == "openai":
            return ApiLLM(
                api_key=config["api_key"],
                model_name=config.get("model_name", "gpt-4")
            )

        else:
            raise ValueError(f"Provider '{provider}' not supported.")