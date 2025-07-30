import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name):
        print(f"🔄 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def encode_chunks(self, chunks):
        embeddings = self.model.encode(chunks, show_progress_bar=True)
        faiss.normalize_L2(embeddings)
        return np.array(embeddings, dtype='float32')

    def encode_query(self, query):
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        return query_embedding.astype('float32')

    def embedding_dim(self):
        return self.model.get_sentence_embedding_dimension()

    def model_class(self):
        return self.model.__class__.__name__