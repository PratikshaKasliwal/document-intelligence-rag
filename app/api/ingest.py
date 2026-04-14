from fastapi import APIRouter, UploadFile, File
from app.services.pdf_loader import extract_text_from_pdf
from app.services.chunker import chunk_text
from app.services.rag_pipeline import ingest_chunks
from app.models.schemas import IngestResponse

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(file: UploadFile = File(...)):
    # 1. Extract text directly from UploadFile
    text = extract_text_from_pdf(file)

    # 2. Chunk the text
    chunks = chunk_text(text)

    # 3. 🚀 VERY IMPORTANT: send chunks to RAG pipeline
    count = ingest_chunks(chunks, filename=file.filename)

    return IngestResponse(
        message=f"PDF '{file.filename}' ingested successfully",
        documents_ingested=count
    )