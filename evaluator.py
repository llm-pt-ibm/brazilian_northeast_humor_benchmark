from multilabel_classification_metrics import MultilabelClassificationMetrics
from text_overlap_metrics import TextOverlapMetrics
from statistics import mean
from json_saver import JSONSaver
from comic_styles_manager import ComicStylesManager
import ast
import json
import os

class Evaluator():

    def __init__(self):
        self.predictions = os.listdir('./predictions')

    def evaluate_models_predictions(self):
        results = {}
        for model_name in self.predictions:
            # TODO remover a linha seguinte depois
            if model_name == 'gemini-2.5-flash':
                continue
            results[model_name] = {
                "punchlines": self.evaluate_punchlines_predictions(model_name),
                "comic_styles": self.evaluate_comic_styles_predictions(model_name),
                #"texts_explanations": self.evaluate_texts_explanations_predictions(model_name)
            }

        JSONSaver.save_json(results, os.path.join('evaluation', 'results.json'))

    def evaluate_punchlines_predictions(self, model_name):
        file_path = os.path.join('predictions', model_name, 'punchlines_predictions.json')

        with open(file_path, 'r', encoding='utf-8') as f:
            punchlines = json.load(f)
        
        dice_results = []
        jaccard_results = []
        levenshtein_results = []

        for video_url in punchlines:
            current_row = punchlines[video_url]
            annotated = current_row['annotated_punchlines']
            predicted = '; '.join(ast.literal_eval(current_row['model_punchlines']))

            dice_results.append(TextOverlapMetrics.dice_similarity(predicted, annotated))
            jaccard_results.append(TextOverlapMetrics.jaccard_similarity(predicted, annotated))
            levenshtein_results.append(TextOverlapMetrics.levenshtein_distance(predicted, annotated))

        punchlines_evaluation = {
            "dice_similarity" : round(mean(dice_results), 2),
            "jaccard_similarity": round(mean(jaccard_results), 2),
            "levenshtein_distance": round(mean(levenshtein_results), 2)
        }

        return punchlines_evaluation

    def evaluate_comic_styles_predictions(self, model_name):
        file_path = os.path.join('predictions', model_name, 'comic_styles_predictions.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            comic_styles_predictions = json.load(f)
        
        comic_styles = ComicStylesManager().get_comic_styles()
        f1_score_trues_and_preds = {comic_style:{'pred': [], 'true': []} for comic_style in comic_styles}
        pred_labels = []
        true_labels = []
        hamming_loss_results = []

        for video_url in comic_styles_predictions:
            current_row = comic_styles_predictions[video_url]

            annotated = current_row['annotated_comic_styles']
            predicted = current_row['model_comic_styles']

            for comic_style in comic_styles:
                f1_score_trues_and_preds[comic_style]['true'].append(int(annotated[comic_style]))
                f1_score_trues_and_preds[comic_style]['pred'].append(int(predicted[comic_style]))

            annot_zeros_and_ones = [int(annotated[comic_style]) for comic_style in comic_styles]
            model_zeros_and_ones = [int(predicted[comic_style]) for comic_style in comic_styles]

            true_labels.append(annot_zeros_and_ones)
            pred_labels.append(model_zeros_and_ones)

            hamming_loss_results.append(MultilabelClassificationMetrics.hamming_loss(y_true=annot_zeros_and_ones, y_pred=model_zeros_and_ones))

        f1_score_results = {
            comic_style: MultilabelClassificationMetrics.f1_score(y_pred = data['pred'], y_true = data['true'], average = 'binary')
            for comic_style, data in f1_score_trues_and_preds.items()
        }

        # Calcular o F1-score macro (média entre classes)
        f1_macro = MultilabelClassificationMetrics.f1_score(y_true = true_labels, y_pred = pred_labels, average='macro')

        # Ou micro (considera todos os 1s e 0s como um único vetor)
        f1_micro = MultilabelClassificationMetrics.f1_score(y_true = true_labels, y_pred = pred_labels, average='micro')

        comic_styles_evaluation = {'f1_score': f1_score_results,
                                   'f1_macro': f1_macro,
                                   'f1_micro': f1_micro,
                                   'hamming_loss': mean(hamming_loss_results)}
        
        return comic_styles_evaluation

    def evaluate_texts_explanations_predictions(self):
        pass