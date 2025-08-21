import pandas as pd
from itertools import cycle

class ExamplesEntriesManager():

    def __init__(self):
        self.dataset = self.get_humorous_text_dataset()
        
    def get_humorous_text_dataset(self):
        df = pd.read_csv('./data/brazilian_ne_annotated_humorous_texts.csv')
        df['corrected_transcription'] = df['corrected_transcription'].apply(lambda text: text.strip())

        return df

    def get_random_punchlines_entries_examples(self, text: str, count: int = 2):
        filtered_df = self.dataset[self.dataset['corrected_transcription'] != text.strip()]
        print(len(filtered_df))
        sample = filtered_df.sample(count)[["corrected_transcription", "punchlines"]]
        examples_list = [
            {"humorous_text": row.corrected_transcription, "punchlines": f'[{row.punchlines.replace(';', ',')}]'}
            for row in sample.itertuples(index=False)
        ]

        return examples_list
    
    def get_random_explanations_entries_examples(self, text: str, count: int = 2):
        filtered_df = self.dataset[self.dataset['corrected_transcription'] != text.strip()]
        print(len(filtered_df))
        sample = filtered_df.sample(count)[["corrected_transcription", "joke_explanation"]]
        examples_list = [
            {"humorous_text": row.corrected_transcription, "explanation": row.joke_explanation}
            for row in sample.itertuples(index=False)
        ]

        return examples_list
    
    def get_random_comic_styles_entries_examples(self, text: str, comic_style: str, count: int = 2):
        filtered_df = self.dataset[self.dataset['corrected_transcription'] != text.strip()]
        groups = {val: df.sample(frac=1).reset_index(drop=True) for val, df in filtered_df.groupby(comic_style)if val in [0, 1]}
        indices = {0: 0, 1: 0}
        examples = []

        for style in cycle([1, 0]):
            if len(examples) >= count:
                break

            idx = indices[style]
            if style in groups and idx < len(groups[style]):
                row = groups[style].iloc[idx]
                indices[style] += 1
                examples.append({"humorous_text": row["corrected_transcription"],"comic_style": str(row[comic_style])})
            else:
                break

        return examples