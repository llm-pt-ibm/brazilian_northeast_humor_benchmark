import os
import time
import json
from comic_styles_manager import ComicStylesManager
from dataset_loader import DatasetLoader
from json_saver import JSONSaver
from llm_prompt_manager import LLMPromptManager
from models_loader import ModelsLoader
import openai

class ExperimentRunner:

    def __init__(self):
        dataset_loader = DatasetLoader('./data/brazilian_ne_annotated_humorous_texts.csv')
        self.df = dataset_loader.load_dataset()
        self.llm_prompt_manager = LLMPromptManager()
        self.comic_styles_manager = ComicStylesManager()
        self.models_loader = ModelsLoader()
        self.json_saver = JSONSaver()

    def execute(self):
        models = self.models_loader.load_models_from_config_file()
        for model in models:
            print(f'--- {model.model_name} ---')
            print('--- Punchlines phase ---')
            self.execute_punchlines_experiment(model)
            print('--- Texts Explanations phase ---')
            self.execute_explanations_experiment(model)
            #print('--- Comic Styles phase ---')
            #self.execute_comic_styles_experiment(model)

    def execute_punchlines_experiment(self, model):
        filename = os.path.join("predictions", model.model_name, 'punchlines_predictions.json')
        predictions = self._load_existing_predictions(filename)

        for i, row in self.df.iterrows():
            video_url = row["video_url"]
            if video_url in predictions:
                continue

            humorous_text = row["corrected_transcription"]
            prompt = self.llm_prompt_manager.get_punchlines_prompt(humorous_text)
            model_output = self._safe_generate(model, prompt)

            predictions[video_url] = {
                "model_name": model.model_name,
                "humorous_text": humorous_text,
                "prompt": prompt,
                "model_punchlines": model_output,
                "annotated_punchlines": row["punchlines"]
            }

            print(f'Step {i + 1} completed.')
            self.json_saver.save_json(predictions, filename)

    def execute_comic_styles_experiment(self, model):
        filename = os.path.join("predictions", model.model_name, 'comic_styles_predictions.json')
        predictions = self._load_existing_predictions(filename)

        comic_styles = self.comic_styles_manager.get_comic_styles()

        for i, row in self.df.iterrows():
            video_url = row["video_url"]
            if video_url in predictions:
                if 'model_comic_styles' in predictions[video_url]:
                    if len(predictions[video_url]['model_comic_styles']) == 8:
                        continue

            humorous_text = row["corrected_transcription"]
            comic_styles_prompts = self.llm_prompt_manager.get_comic_styles_prompts(humorous_text)

            model_outputs = {}
            for comic_style in comic_styles:
                current_prompt = comic_styles_prompts[comic_style]
                model_outputs[comic_style] = self._safe_generate(model, current_prompt)

            predictions[video_url] = {
                "model_name": model.model_name,
                "humorous_text": humorous_text,
                "prompts": comic_styles_prompts,
                "annotated_comic_styles": dict(row[comic_styles]),
                "model_comic_styles": model_outputs
            }

            print(f'Step {i + 1} completed.')
            self.json_saver.save_json(predictions, filename)

    def execute_explanations_experiment(self, model):
        filename = os.path.join("predictions", model.model_name, 'texts_explanations_predictions.json')
        predictions = self._load_existing_predictions(filename)

        for i, row in self.df.iterrows():
            video_url = row["video_url"]
            if video_url in predictions:
                continue

            humorous_text = row["corrected_transcription"]
            prompt = self.llm_prompt_manager.get_text_explanation_prompt(humorous_text)
            model_output = self._safe_generate(model, prompt)

            predictions[video_url] = {
                "model_name": model.model_name,
                "humorous_text": humorous_text,
                "prompt": prompt,
                "model_text_explanation": model_output,
                "annotated_text_explanation": row["joke_explanation"]
            }

            print(f'Step {i + 1} completed.')
            self.json_saver.save_json(predictions, filename)

    def _load_existing_predictions(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _safe_generate(self, model, prompt, max_retries=5, wait_seconds=10):
        retries = 0
        while retries < max_retries:
            try:
                return model.generate(prompt)
            except openai.RateLimitError:
                print(f"Rate limit reached. Waiting {wait_seconds} seconds before retrying...")
                time.sleep(wait_seconds)
                retries += 1
            except Exception as e:
                print(f"Unexpected error during generation: {e}")
                time.sleep(wait_seconds)
                retries += 1
        raise RuntimeError("Max retries exceeded for model.generate()")
