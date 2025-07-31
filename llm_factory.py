from hugging_face_llm import HuggingFaceLLM
from open_ai_llm import OpenAiLLM
from gemini_llm import GeminiLLM
from ibm_cloud_llm import IBMCloudLLM
from ibm_cloud_custom_model import IBMCloudCustomModel

class LLMFactory:
    @staticmethod
    def create_llm(config: dict):
        provider = config.get("provider")

        if provider == "huggingface":
            return HuggingFaceLLM(
                model_name = config['model_name'],
                task = config['task'],
                device = config['device'],
                token = config['token']
            )

        elif provider == "openai":
            return OpenAiLLM(
                api_key=config["api_key"],
                model_name=config.get("model_name")
            )

        elif provider == "gemini":
            return GeminiLLM(
                api_key=config["api_key"],
                model_name=config.get("model_name")
            )

        elif provider == 'ibmcloud':
            return IBMCloudLLM(
                model_id=config.get("model_id"),
                api_key=config["api_key"],
                service_url=config["service_url"],
                project_id=config["project_id"]
            )

        else:
            raise ValueError(f"Provider '{provider}' not supported.")