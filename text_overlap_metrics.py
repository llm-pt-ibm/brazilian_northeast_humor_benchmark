from rouge import Rouge
from nltk.translate.bleu_score import sentence_bleu
import Levenshtein as lev


class TextOverlapMetrics:
    def __init__(self):
        pass

    def jaccard_similarity(self, text1, text2):
        """
        Calculate the Jaccard similarity between two texts.
        """
        set1 = set(text1.split())
        set2 = set(text2.split())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union != 0 else 0
    

    def rouge_score(self, text1, text2):
        """
        Calculate the ROUGE score between two texts.
        """
        rouge = Rouge()
        scores = rouge.get_scores(text1, text2)
        return scores[0]['rouge-l']['f']

    def bleu_score(self, text1, text2):
        """
        Calculate the BLEU score between two texts.
        """
        
        reference = text2.split()
        candidate = text1.split()
        return sentence_bleu([reference], candidate)
    
    def f1_score(self, text1, text2):
        """
        Calculate the F1 score between two texts.
        """
        set1 = set(text1.split())
        set2 = set(text2.split())
        intersection = len(set1.intersection(set2))
        precision = intersection / len(set1) if len(set1) != 0 else 0
        recall = intersection / len(set2) if len(set2) != 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
        return f1
    

    def dice_similarity(self, text1, text2):
        """
        Calculate the Dice similarity between two texts.
        """
        set1 = set(text1.split())
        set2 = set(text2.split())
        intersection = len(set1.intersection(set2))
        return (2 * intersection) / (len(set1) + len(set2)) if (len(set1) + len(set2)) != 0 else 0
    
    def levenstein_distance(self, text1, text2):
        """
        Calculate the Levenshtein distance between two texts.
        """
        words1 = text1.split()
        words2 = text2.split()
        return lev.distance(words1, words2)
