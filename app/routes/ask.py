
from fastapi import APIRouter
from pydantic import BaseModel

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../chatbot-assistant/scripts')))
from query_assistant import SacrificeValidationChatbot

router = APIRouter()

chatbot = SacrificeValidationChatbot()


class QueryRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_question(req: QueryRequest):
    lang = chatbot.detect_language(req.question)
    context_items = chatbot.search_knowledge_base(req.question)
    answer = chatbot.generate_response(req.question, context_items, lang)
    return {"answer": answer}
