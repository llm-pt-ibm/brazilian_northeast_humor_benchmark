from string_utils import StringUtils
import editdistance

class TextOverlapMetrics:

    def __init__(self):
        pass

    @staticmethod
    def jaccard_similarity(text1, text2):
        """
        Calculate the Jaccard similarity between two texts.
        """
        text1, text2 = StringUtils.normalize_text(text1), StringUtils.normalize_text(text2)
        set1 = set(text1.split())
        set2 = set(text2.split())
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union != 0 else 0

    @staticmethod
    def dice_similarity(text1, text2):
        """
        Calculate the Dice similarity between two texts.
        """
        text1, text2 = StringUtils.normalize_text(text1), StringUtils.normalize_text(text2)
        set1 = set(text1.split())
        set2 = set(text2.split())
        intersection = len(set1.intersection(set2))
        return (2 * intersection) / (len(set1) + len(set2)) if (len(set1) + len(set2)) != 0 else 0

    @staticmethod
    def levenshtein_distance(text1, text2):
        """
        Calculate the Levenshtein distance between two texts at the word level.
        """
        text1, text2 = StringUtils.normalize_text(text1), StringUtils.normalize_text(text2)
        tokens1 = text1.strip().split()
        tokens2 = text2.strip().split()

        return editdistance.eval(tokens1, tokens2)

