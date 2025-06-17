import os
import json
from comic_styles_manager import ComicStylesManager
from dataset_loader import DatasetLoader
from llm_prompt_manager import LLMPromptManager
from models_loader import ModelsLoader

class ExperimentRunner:

    def __init__(self):
        dataset_loader = DatasetLoader('./data/brazilian_ne_annotated_humorous_texts.csv')
        self.df = dataset_loader.load_dataset().sample(2)
        self.llm_prompt_manager = LLMPromptManager()
        self.comic_styles_manager = ComicStylesManager()
        self.models_loader = ModelsLoader()

    def execute(self):
        models = self.models_loader.load_models_from_config_file()
        for model in models:
            self.execute_punchlines_experiment(model)
            # self.execute_comic_styles_experiment(model)
            # self.execute_explanations_experiment(model)

    def _prepare_results_path(self, model, experiment_name, filename="results.json"):
        dir_path = os.path.join("results", model.model_name, experiment_name)
        os.makedirs(dir_path, exist_ok=True)
        return os.path.join(dir_path, filename)

    def execute_punchlines_experiment(self, model):
        results_path = self._prepare_results_path(model, "punchlines")
        results = {}

        for i, row in self.df.iterrows():
            video_url = row["video_url"]
            humorous_text = row["corrected_transcription"]
            prompt = self.llm_prompt_manager.get_punchlines_prompt(humorous_text)
            model_output = model.generate(prompt)

            results[video_url] = {
                "model_name": model.model_name,
                "humorous_text": humorous_text,
                "prompt": prompt,
                "model_punchlines": model_output,
                "annotated_punchlines": row["punchlines"]
            }

        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    def execute_comic_styles_experiment(self, model):
        results_path = self._prepare_results_path(model, "comic_styles")
        comic_styles = self.comic_styles_manager.get_comic_styles()
        annotated_comic_styles = self.df[comic_styles]
        # TODO: Implementar lógica
        pass

    def execute_explanations_experiment(self, model):
        results_path = self._prepare_results_path(model, "explanations")
        explanations_prompt = self.llm_prompt_manager.get_text_explanation_prompt()
        annotated_explanations = self.df["joke_explanation"]
        # TODO: Implementar lógica
        pass