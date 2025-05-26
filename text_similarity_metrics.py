from sentence_transformers import SentenceTransformer, util

class TextSimilarityMetrics:
    def __init__(self):
        pass

    def paraphrase_mpnet_similarity(self, text1, text2):
        """
        Calculate the paraphrase MPNet similarity between two texts.
        """
        return self.cos_similarity('paraphrase-mpnet-base-v2', text1, text2)
    
    def all_mpnet_similarity(self, text1, text2):
        """
        Calculate the all MPNet similarity between two texts.
        """
        return self.cos_similarity('all-mpnet-base-v2', text1, text2)

    def all_minilm_similarity(self, text1, text2):
        """
        Calculate the all MiniLM similarity between two texts.
        """
        return self.cos_similarity('all-MiniLM-L6-v2', text1, text2)

    def cos_similarity(self, model, text1, text2):
        """
        Calculate the cosine similarity between two texts using Sentence Transformers.
        """
        model = SentenceTransformer(model)
        embeddings1 = model.encode(text1)
        embeddings2 = model.encode(text2)
        cosine_similarity = util.pytorch_cos_sim(embeddings1, embeddings2)
        return cosine_similarity.item()