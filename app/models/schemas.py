from pydantic import BaseModel
from typing import List

class HealthResponse(BaseModel):
    status: str
    env: str


class IngestResponse(BaseModel):
    message: str
    documents_ingested: int


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]