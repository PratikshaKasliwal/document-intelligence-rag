from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def embed_documents(self, texts: list[str]):
        return self.model.encode(texts)

    def embed_query(self, query: str):
        return self.model.encode(query)


# ✅ SINGLETON INSTANCE
embedding_model = EmbeddingModel()