from comic_styles_manager import ComicStylesManager
from dataset_loader import DatasetLoader
from llm_factory import LLMFactory
from llm_prompt_manager import LLMPromptManager
import os

class ExperimentRunner:

    def __init__(self):
        dataset_loader = DatasetLoader('/data/brazilian_ne_annotated_humorous_texts.csv')
        self.df = dataset_loader.load_dataset()
        self.llm_prompt_manager = LLMPromptManager()
        self.comic_styles_manager = ComicStylesManager()

    def execute(self):
        # Carrega os LLMs
        # Executa os modelos com os prompts
        # Salva os resultados

        models = []
        for model in models:
            os.makedirs(model.model_name)
            self.execute_punchlines_experiment(model)
    
    def execute_punchlines_experiment(self, model):
        punchlines_results_path = os.makedirs(os.path.join(model.name, 'punchlines'))
        punchlines_prompt = self.llm_prompt_manager.get_punchlines_prompt()

        annotated_punchlines = self.df['punchlines']
        
        pass

    def execute_comic_styles_experiment(self, model):
        comic_styles_results_path = os.makedirs(os.path.join(model.name, 'comic_styles'))
        comic_styles = self.comic_styles_manager.get_comic_styles()

        annotated_comic_styles = self.df[comic_styles]

        pass

    def execute_explanations_experiment(self, model):
        explanations_results_path = os.makedirs(os.path.join(model.name, 'explanations'))
        explanations_prompt = self.llm_prompt_manager.get_text_explanation_prompt()

        annotated_explanations = self.df['joke_explanation']
        pass
