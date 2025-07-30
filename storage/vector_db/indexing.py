import faiss  # type: ignore
import numpy as np
from typing import Tuple

class FaissIndex:
    def __init__(self, dim: int) -> None:
        self.index = faiss.IndexFlatIP(dim)  # type: ignore

    def add_embeddings(self, embeddings: np.ndarray) -> None:
        self.index.add(embeddings)  # type: ignore

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        scores, indices = self.index.search(query_embedding, top_k)  # type: ignore
        return scores[0], indices[0]  # type: ignore