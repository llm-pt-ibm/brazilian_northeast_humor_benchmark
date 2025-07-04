from comic_styles_manager import ComicStylesManager
from json_saver import JSONSaver
from judge_model import JudgeModel
from multilabel_classification_metrics import MultilabelClassificationMetrics
from statistics import mean
from string_utils import StringUtils
from text_overlap_metrics import TextOverlapMetrics

import json
import os

class Evaluator():

    def __init__(self):
        pass

    def evaluate_models_predictions(self):
        def load_json(path):
            return json.load(open(path, 'r', encoding='utf-8')) if os.path.exists(path) else {}

        def save():
            JSONSaver.save_json(results, aggregate_path)
            JSONSaver.save_json(all_individual_metrics, individual_path)

        def evaluate_phase(model_name, phase_key, eval_func, message):
            if phase_key not in results[model_name]:
                print(message)
                agg, ind = eval_func(model_name)
                results[model_name][phase_key] = agg
                all_individual_metrics[model_name][phase_key] = ind
                save()

        aggregate_path = os.path.join('evaluation', 'aggregate_metrics.json')
        individual_path = os.path.join('evaluation', 'individual_metrics.json')
        predictions = os.listdir('./predictions')

        results = load_json(aggregate_path)
        all_individual_metrics = load_json(individual_path)

        phases_by_priority = [
            ("punchlines", self.evaluate_punchlines_predictions, "--- Text Overlap Metrics phase ---"),
            ("comic_styles", self.evaluate_comic_styles_predictions, "--- Comic Styles Classification Metrics phase ---"),
            ("texts_explanations", self.evaluate_texts_explanations_predictions, "--- Texts Explanations Agreement Metrics phase ---"),
        ]

        for phase_key, eval_func, message in phases_by_priority:
            for model_name in predictions:
                results.setdefault(model_name, {})
                all_individual_metrics.setdefault(model_name, {})
                evaluate_phase(model_name, phase_key, eval_func, f'--- {model_name} ---\n{message}')

    def evaluate_punchlines_predictions(self, model_name):
        file_path = os.path.join('predictions', model_name, 'punchlines_predictions.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            punchlines = json.load(f)
        
        dice_results = []
        jaccard_results = []
        levenshtein_results = []
        individual_metrics = []

        for video_url in punchlines:
            current_row = punchlines[video_url]
            annotated = current_row['annotated_punchlines']
            formatted_model_punchlines = StringUtils().extract_list_of_strings_from_text(current_row['model_punchlines'])
            predicted = '; '.join(formatted_model_punchlines)

            dice = TextOverlapMetrics.dice_similarity(predicted, annotated)
            jaccard = TextOverlapMetrics.jaccard_similarity(predicted, annotated)
            levenshtein = TextOverlapMetrics.levenshtein_distance(predicted, annotated)

            dice_results.append(dice)
            jaccard_results.append(jaccard)
            levenshtein_results.append(levenshtein)

            individual_metrics.append({
                "video_url": video_url,
                **current_row,
                "dice_similarity": dice,
                "jaccard_similarity": jaccard,
                "levenshtein_distance": levenshtein,
            })

        punchlines_evaluation = {
            "dice_similarity": mean(dice_results),
            "jaccard_similarity": mean(jaccard_results),
            "levenshtein_distance": mean(levenshtein_results)
        }

        return punchlines_evaluation, individual_metrics

    def evaluate_comic_styles_predictions(self, model_name):
        file_path = os.path.join('predictions', model_name, 'comic_styles_predictions.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            comic_styles_predictions = json.load(f)
        
        comic_styles = ComicStylesManager().get_comic_styles()
        f1_score_trues_and_preds = {comic_style: {'pred': [], 'true': []} for comic_style in comic_styles}
        pred_labels = []
        true_labels = []
        hamming_loss_results = []

        individual_metrics = []

        for video_url in comic_styles_predictions:
            current_row = comic_styles_predictions[video_url]
            annotated = current_row['annotated_comic_styles']
            predicted = current_row['model_comic_styles']

            for comic_style in comic_styles:
                f1_score_trues_and_preds[comic_style]['true'].append(int(annotated[comic_style]))
                f1_score_trues_and_preds[comic_style]['pred'].append(int(predicted[comic_style]))

            annot_ones = [int(annotated[comic_style]) for comic_style in comic_styles]
            pred_ones = [int(predicted[comic_style]) for comic_style in comic_styles]

            true_labels.append(annot_ones)
            pred_labels.append(pred_ones)

            hamming = MultilabelClassificationMetrics.hamming_loss(y_true=annot_ones, y_pred=pred_ones)
            hamming_loss_results.append(hamming)

            individual_metrics.append({
                "video_url": video_url,
                **current_row,
                "hamming_loss": hamming,
            })

        f1_binary = {comic_style: MultilabelClassificationMetrics.f1_score(
                y_pred=data['pred'], y_true=data['true'], average='binary')
                for comic_style, data in f1_score_trues_and_preds.items()}

        f1_macro = MultilabelClassificationMetrics.f1_score(y_true=true_labels, y_pred=pred_labels, average='macro')
        f1_micro = MultilabelClassificationMetrics.f1_score(y_true=true_labels, y_pred=pred_labels, average='micro')

        comic_styles_evaluation = {
            'f1_score': f1_binary,
            'f1_macro': f1_macro,
            'f1_micro': f1_micro,
            'hamming_loss': mean(hamming_loss_results)
        }

        return comic_styles_evaluation, individual_metrics

    def evaluate_texts_explanations_predictions(self, model_name):
        input_path = os.path.join('predictions', model_name, 'texts_explanations_predictions.json')
        output_path = os.path.join('evaluation', 'texts_explanations_evaluation_results.json')

        with open(input_path, 'r', encoding='utf-8') as f:
            texts_explanations = json.load(f)

        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                processed_results = json.load(f)
        else:
            processed_results = {}

        if model_name not in processed_results:
            processed_results[model_name] = {}

        judge_model = JudgeModel()
        agreement_level_results = []
        individual_metrics = []

        for video_url, current_row in texts_explanations.items():
            if video_url in processed_results[model_name]:
                result = processed_results[model_name][video_url]
                agreement_level_results.append(int(result['judge_model_results']['nivel_concordancia']))
                individual_metrics.append(result)
                continue 

            annotated = current_row['annotated_text_explanation']
            predicted = current_row['model_text_explanation']

            try:
                agreement_level_response_json = json.loads(judge_model.get_agreement_level(annotated_text=annotated, model_text=predicted))
                current_agreement_level = int(agreement_level_response_json['nivel_concordancia'])
            except Exception as e:
                print(f"[Erro] Falha ao avaliar {video_url}: {e}")
                continue

            current_result = {
                "video_url": video_url,
                **current_row,
                "judge_model_results": agreement_level_response_json,
            }

            processed_results[model_name][video_url] = current_result
            agreement_level_results.append(current_agreement_level)
            individual_metrics.append(current_result)

            print(f'Step {model_name} - {video_url} completed')
            JSONSaver.save_json(processed_results, output_path)

        texts_explanations_results = mean(agreement_level_results) if agreement_level_results else 0

        return texts_explanations_results, individual_metrics