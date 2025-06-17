from llm_factory import LLMFactory
import yaml

class ModelsLoader():

    def __init__(self, config_path: str = "./config/model_deployment.yaml"):
        self.config_path = config_path

    def load_models_from_config_file(self):
        with open(self.config_path, "r") as f:
            config_data = yaml.safe_load(f)

        models = [LLMFactory.create_llm(model_config) for model_config in config_data.get("models", [])]
        return models
