import numpy as np
import faiss  # type: ignore
from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingModel:
    def __init__(self, model_name: str) -> None:
        print(f"🔄 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def encode_chunks(self, chunks: List[str]) -> np.ndarray:
        embeddings = self.model.encode(chunks, show_progress_bar=True)  # type: ignore
        faiss.normalize_L2(embeddings)  # type: ignore
        return np.array(embeddings, dtype='float32')

    def encode_query(self, query: str) -> np.ndarray:
        query_embedding = self.model.encode([query])  # type: ignore
        faiss.normalize_L2(query_embedding)  # type: ignore
        return query_embedding.astype('float32')

    def embedding_dim(self) -> int:
        dim = self.model.get_sentence_embedding_dimension()
        return dim if dim is not None else 384  # Default dimension for MiniLM

    def model_class(self) -> str:
        return self.model.__class__.__name__