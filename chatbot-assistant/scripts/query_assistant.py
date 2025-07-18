import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv
import os
import gc
from typing import Optional

load_dotenv()


class OptimizedAssistant:
    def __init__(self):
        self.model: Optional[SentenceTransformer] = None
        self.index: Optional[faiss.Index] = None
        self.chunks: Optional[list] = None

        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        self.llm = genai.GenerativeModel("gemini-1.5-flash-latest")

    def _load_model(self):
        """Lazy load the sentence transformer model"""
        if self.model is None:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def _load_index(self):
        """Lazy load the FAISS index"""
        if self.index is None:
            self.index = faiss.read_index("./dataset/faiss.index")

    def _load_chunks(self):
        """Lazy load the chunks data"""
        if self.chunks is None:
            with open("./dataset/chunks.json", "r", encoding="utf-8") as f:
                self.chunks = json.load(f)

    def _cleanup_after_embedding(self):
        """Clean up model after embedding to free memory"""
        if self.model is not None:
            del self.model
            self.model = None
            gc.collect()

    def answer_question(self, query: str, k: int = 3) -> str:
        try:
            self._load_model()
            self._load_index()
            self._load_chunks()

            query_embedding = self.model.encode([query])

            self._cleanup_after_embedding()

            D, I = self.index.search(
                np.array(query_embedding).astype(np.float32), k)

            retrieved_chunks = [self.chunks[idx]["content"] for idx in I[0]]
            context = "\n\n".join(retrieved_chunks)

            prompt = f"""
You're an AI assistant helping users learn more about Zakaria Goumri.

Below is some background information. Use it to give a helpful, polite, and friendly response to the user's question.

--- CONTEXT ---
{context}
--- END CONTEXT ---

Now answer this question as if you're having a casual, respectful conversation:

{query}

Respond:
"""

            response = self.llm.generate_content(prompt)
            return response.text

        except Exception as e:
            return f"Error processing question: {e}"


assistant = OptimizedAssistant()


def answer_question(query: str, k: int = 3) -> str:
    return assistant.answer_question(query, k)
