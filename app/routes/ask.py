
from fastapi import APIRouter
from pydantic import BaseModel

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../chatbot-assistant/scripts')))
from query_assistant import answer_question

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_question(req: QueryRequest):
    answer = answer_question(req.question)
    return {"answer": answer}
