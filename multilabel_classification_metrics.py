from sklearn.metrics import f1_score, hamming_loss

class MultilabelClassificationMetrics:

    @staticmethod
    def f1_score(y_true, y_pred, average = None):
        """
        Calculate F1 score for multilabel classification using sklearn.
        """
        return f1_score(y_true = y_true, y_pred = y_pred, average = average)

    @staticmethod
    def hamming_loss(y_true, y_pred):
        """
        Calculate Hamming loss for multilabel classification.
        """
        return hamming_loss(y_pred = y_pred, y_true = y_true)
