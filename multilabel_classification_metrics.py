from sklearn.metrics import f1_score, hamming_loss

class MultilabelClassificationMetrics:
    def __init__(self):
        pass

    def f1_score(self, y_true, y_pred):
        """
        Calculate F1 score for multilabel classification using sklearn.
        """
        return f1_score(y_true, y_pred)

    def hamming_loss(self, y_true, y_pred):
        """
        Calculate Hamming loss for multilabel classification.
        """
        return hamming_loss(y_pred=y_pred, y_true=y_true)
