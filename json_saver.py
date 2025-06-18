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
