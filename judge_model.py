from models_loader import ModelsLoader
from llm_prompt_manager import LLMPromptManager

class JudgeModel:

    def __init__(self):
        self.judging_model = ModelsLoader(config_path = './config/judge_model_config.yaml').load_models_from_config_file()
        self.llm_prompt_manager = LLMPromptManager()

    def get_agreement_level(self, annotated_text, model_text):
        prompt = self.llm_prompt_manager.get_agreement_level_prompt(annotated_explanation=annotated_text, model_explanation=model_text)
        agreement_level_from_judge_llm = self.judging_model.generate(prompt)

        return agreement_level_from_judge_llm
