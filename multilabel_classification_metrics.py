from sklearn.metrics import f1_score, hamming_loss, accuracy_score


class MultilabelClassificationMetrics:
    def __init__(self):
        pass
        

    def f1_score(self, y_true, y_pred):
        """
        Calculate F1 score for multilabel classification using sklearn.
        """
        return f1_score(y_true, y_pred)

    def f1_score_weighted(self, y_true, y_pred):
        """
        Calculate weighted F1 score for multilabel classification using sklearn.
        """
        return f1_score(y_true, y_pred, average='weighted')
    
    def f1_score_micro(self, y_true, y_pred):
        """
        Calculate micro F1 score for multilabel classification using sklearn.
        """
        return f1_score(y_true, y_pred, average='micro')
    
    def f1_score_macro(self, y_true, y_pred):
        """
        Calculate macro F1 score for multilabel classification using sklearn.
        """
        return f1_score(y_true, y_pred, average='macro')

    def hamming_loss(self, y_true, y_pred):
        """
        Calculate Hamming loss for multilabel classification.
        """
        return hamming_loss(y_pred=y_pred, y_true=y_true)
   
    def accuracy_score(self, y_true, y_pred):
        """
        Calculate accuracy score for multilabel classification.
        """
        return accuracy_score(y_true, y_pred)