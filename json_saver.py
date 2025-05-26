import json
import os

class JSONSaver:
    @staticmethod
    def save_results(data, filepath):
        """
        Salva os resultados no formato JSON no caminho especificado.

        Args:
            data (dict): Dados a serem salvos.
            filepath (str): Caminho do arquivo JSON.
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    @staticmethod
    def prepare_results(
        model_name, style_scores, punchline_scores, explanation_scores
    ):
        """
        Prepara os resultados para salvamento no formato JSON.

        Args:
            model_name (str): Nome do modelo avaliado.
            style_scores (dict): Pontuações de estilo.
            punchline_scores (float): Pontuação de punchlines.
            explanation_scores (float): Pontuação de explicação.

        Returns:
            dict: Estrutura de resultados formatada.
        """
        return {
            "model_name": model_name,
            "style_scores": style_scores,
            "punchline_scores": punchline_scores,
            "explanation_scores": explanation_scores,
        }
