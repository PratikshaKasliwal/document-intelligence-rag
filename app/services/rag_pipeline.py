import os
from groq import Groq
from app.core.embeddings import embedding_model
from app.core.vector_store import vector_store  # ✅ IMPORT SINGLETON

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ingest_chunks(chunks: list[str], filename: str) -> int:
    embeddings = embedding_model.embed_documents(chunks)
    
    # Create a list of dictionaries, one for each chunk
    metadatas = [{"filename": filename} for _ in chunks]
    
    # Pass metadatas to the vector store
    vector_store.add_documents(embeddings, chunks, metadatas=metadatas)
    return len(chunks)

def answer_question(question: str, top_k: int = 5):
    query_embedding = embedding_model.embed_query(question)
    
    # Now returns list of dicts: [{"text": "...", "filename": "..."}]
    retrieved_results = vector_store.search(query_embedding, top_k)

    if not retrieved_results:
        return "I couldn't find any relevant information.", []

    # 1. Prepare context for LLM
    context_text = "\n\n---\n\n".join([res["text"] for res in retrieved_results])

    # 2. Get ONLY the filename for the response
    filenames = list(set([res["filename"] for res in retrieved_results]))

    prompt = f"""
Answer the question using ONLY the context below.
If not found, say "Not in document".

CONTEXT:
{context_text}

QUESTION:
{question}
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        answer = completion.choices[0].message.content
    except Exception as e:
        answer = f"API Error: {str(e)}"

    return answer, filenames