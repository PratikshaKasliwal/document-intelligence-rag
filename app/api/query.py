from fastapi import APIRouter
from app.services.rag_pipeline import answer_question
from app.models.schemas import QueryRequest, QueryResponse

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query_documents(request: QueryRequest):
    answer, sources = answer_question(request.question)
    return QueryResponse(
        answer=answer,
        sources=sources
    )