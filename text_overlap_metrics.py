from string_utils import StringUtils

class TextOverlapMetrics:

    def __init__(self):
        pass

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

