import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []
        self.metadata = []

        
    def add_documents(self, embeddings, documents, metadatas=None):
        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)
        self.documents.extend(documents)
        
        # Store metadata if provided, otherwise store "Unknown"
        if metadatas:
            self.metadata.extend(metadatas)
        else:
            self.metadata.extend([{"filename": "Unknown"}] * len(documents))



    def search(self, query_embedding, top_k: int):
        if len(self.documents) == 0:
            return []

        query_embedding = np.array([query_embedding]).astype("float32")
        top_k = min(top_k, len(self.documents))

        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for i in indices[0]:
            if i != -1 and i < len(self.documents):
                if i < len(self.metadata):
                    meta = self.metadata[i]
                # Handle if meta is a dict or just a string
                    fname = meta.get("filename") if isinstance(meta, dict) else meta
                else:
                    fname = "Unknown Source"

                results.append({
                    "text": self.documents[i],
                    "filename": fname or "Unknown Source"
                })
        return results

# # ✅ SINGLE SHARED INSTANCE (VERY IMPORTANT)
vector_store = VectorStore(dim=384)