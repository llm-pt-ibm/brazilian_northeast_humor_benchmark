from collections import Counter
from comic_styles_manager import ComicStylesManager
from json_saver import JSONSaver
from judge_model import JudgeModel
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from sklearn.preprocessing import MultiLabelBinarizer
from statistics import mean
from string_utils import StringUtils
from text_overlap_metrics import TextOverlapMetrics

import json
import os

class Evaluator():

    def __init__(self):
        pass

    def evaluate_all_scenarios(self):
        predictions_root = './predictions'
        scenarios = [
            d for d in os.listdir(predictions_root)
            if os.path.isdir(os.path.join(predictions_root, d))
        ]

        for scenario in scenarios:
            print(f"\n=== Avaliando cenário: {scenario} ===")
            self.evaluate_models_predictions(scenario)

    def evaluate_models_predictions(self, scenario_name):
        def load_json(path):
            return json.load(open(path, 'r', encoding='utf-8')) if os.path.exists(path) else {}

        def save():
            JSONSaver.save_json(results, aggregate_path)
            JSONSaver.save_json(all_individual_metrics, individual_path)

        def evaluate_phase(model_name, phase_key, eval_func, message):
            print(f'--- {model_name} ---\n{message}')
            agg, ind = eval_func(model_name, scenario_name)
            results[model_name][phase_key] = agg
            all_individual_metrics[model_name][phase_key] = ind
            save()

        scenario_predictions = os.path.join('predictions', scenario_name)
        scenario_evaluation = os.path.join('evaluation', scenario_name)
        os.makedirs(scenario_evaluation, exist_ok=True)

        aggregate_path = os.path.join(scenario_evaluation, 'aggregate_metrics.json')
        individual_path = os.path.join(scenario_evaluation, 'individual_metrics.json')

        models = os.listdir(scenario_predictions)

        results = load_json(aggregate_path)
        all_individual_metrics = load_json(individual_path)

        phases_by_priority = [
            ("punchlines", self.evaluate_punchlines_predictions, "--- Text Overlap Metrics phase ---"),
            ("comic_styles", self.evaluate_comic_styles_predictions, "--- Comic Styles Classification Metrics phase ---"),
            ("texts_explanations", self.evaluate_texts_explanations_predictions, "--- Texts Explanations Agreement Metrics phase ---"),
        ]

        for phase_key, eval_func, message in phases_by_priority:
            for model_name in models:
                results.setdefault(model_name, {})
                all_individual_metrics.setdefault(model_name, {})
                evaluate_phase(model_name, phase_key, eval_func, message)

    def evaluate_punchlines_predictions(self, model_name, scenario_name):
        file_path = os.path.join('predictions', scenario_name, model_name, 'punchlines_predictions.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            punchlines = json.load(f)
        
        dice_results = []
        individual_metrics = []

        total = len(punchlines)
        hits_original_format = 0
        hits_after_treatment = 0

        for video_url in punchlines:
            current_row = punchlines[video_url]
            annotated = current_row['annotated_punchlines']
            raw_model_output = current_row['model_punchlines']
            prompt = current_row['prompt']

            is_original_valid = StringUtils.is_valid_list_of_strings(raw_model_output)
            if is_original_valid:
                hits_original_format += 1

            cleaned_prediction = StringUtils.remove_prompt_from_model_answer(
                prompt=prompt,
                model_answer=raw_model_output
            )
            formatted_model_punchlines = StringUtils.extract_list_of_strings_from_text(cleaned_prediction)
            is_after_treatment_valid = bool(formatted_model_punchlines)

            if is_after_treatment_valid:
                hits_after_treatment += 1

            predicted = '; '.join(formatted_model_punchlines)

            if is_after_treatment_valid:
                dice = TextOverlapMetrics.dice_similarity(predicted, annotated)
                dice_results.append(dice)
            else:
                dice = None

            individual_metrics.append({
                "video_url": video_url,
                **current_row,
                "raw_model_output": raw_model_output,
                "cleaned_prediction": cleaned_prediction, 
                "formatted_model_punchlines": formatted_model_punchlines, 
                "dice_similarity": dice,
                "is_original_format_valid": is_original_valid,
                "is_after_treatment_valid": is_after_treatment_valid
            })

        if dice_results:
            avg_dice = mean(dice_results)
        else:
            avg_dice = None

        punchlines_evaluation = {
            "dice_similarity": avg_dice,
            "hit_rate_pre_treatment": hits_original_format / total,
            "hit_rate": hits_after_treatment / total
        }

        return punchlines_evaluation, individual_metrics

    def evaluate_comic_styles_predictions(self, model_name, scenario_name):
        file_path = os.path.join('predictions', scenario_name, model_name, 'comic_styles_predictions.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            comic_styles_predictions = json.load(f)

        comic_styles = ComicStylesManager().get_comic_styles()
        style_keys = list(comic_styles)

        f1_data = {style: {'true': [], 'pred': []} for style in style_keys}
        true_labels = []
        pred_labels = []

        total_predictions = 0
        hits_original_format = 0
        hits_after_treatment = 0
        invalid_predictions = 0
        empty_response_counter = Counter()
        individual_metrics = []

        for video_url, current_row in comic_styles_predictions.items():
            annotated = current_row['annotated_comic_styles']
            predicted = current_row['model_comic_styles']
            humorous_text = current_row['humorous_text']
            prompts = current_row['prompts']

            valid_true = []
            valid_pred = []

            for style in style_keys:
                raw_true_val = annotated.get(style)
                raw_pred_val = predicted.get(style)
                current_prompt = prompts.get(style)
                total_predictions += 1

                if raw_pred_val in {"0", "1"}:
                    hits_original_format += 1

                if raw_pred_val is None or str(raw_pred_val).strip() == "":
                    invalid_predictions += 1
                    empty_response_counter[style] += 1
                    continue
                if raw_true_val is None or str(raw_true_val).strip() == "":
                    invalid_predictions += 1
                    continue

                pred_val = StringUtils.remove_prompt_from_model_answer(
                    prompt=current_prompt,
                    model_answer=raw_pred_val
                )
                pred_val = StringUtils.extract_binary_digit(raw_pred_val)
                true_val = StringUtils.extract_binary_digit(raw_true_val)

                if pred_val is not None and true_val is not None:
                    hits_after_treatment += 1

                    pred_int = int(pred_val)
                    true_int = int(true_val)

                    f1_data[style]['true'].append(true_int)
                    f1_data[style]['pred'].append(pred_int)

                    valid_true.append(true_int)
                    valid_pred.append(pred_int)

                    individual_metrics.append({
                        "video_url": video_url,
                        "comic_style": style,
                        "prompt": current_prompt,
                        "true_label": true_int,
                        "pred_label": pred_int,
                        "is_correct": int(pred_int == true_int),
                        "humorous_text": humorous_text,
                        "model_name": model_name
                    })
                else:
                    invalid_predictions += 1

            if valid_true:
                true_labels.append(valid_true)
                pred_labels.append(valid_pred)

        f1_binary = {}
        precision_binary = {}
        recall_binary = {}
        accuracy_binary = {}

        for style, data in f1_data.items():
            if data['true'] and data['pred']:
                true_vals = data['true']
                pred_vals = data['pred']

                f1_binary[style] = f1_score(true_vals, pred_vals, average='binary', zero_division=0)
                precision_binary[style] = precision_score(true_vals, pred_vals, average='binary', zero_division=0)
                recall_binary[style] = recall_score(true_vals, pred_vals, average='binary', zero_division=0)
                accuracy_binary[style] = accuracy_score(true_vals, pred_vals)

        if true_labels and pred_labels:
            mlb = MultiLabelBinarizer(classes=list(range(len(style_keys))))
            true_binary = mlb.fit_transform(true_labels)
            pred_binary = mlb.transform(pred_labels)

            f1_macro = f1_score(true_binary, pred_binary, average='macro', zero_division=0)
            f1_micro = f1_score(true_binary, pred_binary, average='micro', zero_division=0)
        else:
            f1_macro = None
            f1_micro = None

        omission_rate = invalid_predictions / total_predictions if total_predictions > 0 else 0

        comic_styles_evaluation = {
            'f1_score': f1_binary,
            'precision': precision_binary,
            'recall': recall_binary,
            'accuracy': accuracy_binary,
            'f1_macro': f1_macro,
            'f1_micro': f1_micro,
            'hit_rate_pre_treatment': hits_original_format / total_predictions if total_predictions > 0 else 0,
            'hit_rate': hits_after_treatment / total_predictions if total_predictions > 0 else 0,
            'omission_rate': omission_rate
        }

        return comic_styles_evaluation, individual_metrics

    def evaluate_texts_explanations_predictions(self, model_name, scenario_name):
        input_path = os.path.join('predictions', scenario_name, model_name, 'texts_explanations_predictions.json')
        output_path = os.path.join('evaluation', scenario_name, 'texts_explanations_evaluation_results.json')

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

        for idx, (video_url, current_row) in enumerate(texts_explanations.items()):
            prompt = current_row['prompt']

            if video_url in processed_results[model_name]:
                result = processed_results[model_name][video_url]
                result = StringUtils.remove_prompt_from_model_answer(prompt=prompt, model_answer=result)
                agreement_level_results.append(int(result['judge_model_results']['nivel_concordancia']))
                individual_metrics.append(result)
                continue

            annotated = current_row['annotated_text_explanation']
            predicted = current_row['model_text_explanation']
            predicted = StringUtils.remove_prompt_from_model_answer(prompt=prompt, model_answer=predicted)

            try:
                agreement_level_response_json = json.loads(
                    judge_model.get_agreement_level(
                        annotated_text=annotated,
                        model_text=predicted
                    )
                )
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

            print(f'Step {idx} - {model_name} completed.')
            JSONSaver.save_json(processed_results, output_path)

        texts_explanations_results = mean(agreement_level_results) if agreement_level_results else None
        return texts_explanations_results, individual_metrics
