import faiss

class FaissIndex:
    def __init__(self, dim):
        self.index = faiss.IndexFlatIP(dim)

    def add_embeddings(self, embeddings):
        self.index.add(embeddings)

    def search(self, query_embedding, top_k=5):
        scores, indices = self.index.search(query_embedding, top_k)
        return scores[0], indices[0]