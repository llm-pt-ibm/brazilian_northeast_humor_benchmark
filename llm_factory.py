from hugging_face_llm import HuggingFaceLLM
from open_ai_llm import OpenAiLLM
from gemini_llm import GeminiLLM

class LLMFactory:
    @staticmethod
    def create_llm(config: dict):
        provider = config.get("provider")

        if provider == "huggingface":
            return HuggingFaceLLM(**{
                key: config[key]
                for key in ["model_name", "task", "device", "token"]
                if key in config}
            )

        elif provider == "openai":
            return OpenAiLLM(
                api_key=config["api_key"],
                model_name=config.get("model_name", "gpt-4")
            )

        elif provider == "gemini":
            return GeminiLLM(
                api_key=config["api_key"],
                model_name=config.get("model_name", "gemini-pro")
            )

        else:
            raise ValueError(f"Provider '{provider}' not supported.")