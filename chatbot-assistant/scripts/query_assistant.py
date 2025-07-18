import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv
import os
import gc
from typing import Optional, List, Dict
import re

load_dotenv()


class SacrificeValidationChatbot:
    def __init__(
        self,
        index_path: str = "/home/zaki/Projects/junction/junction-ai/chatbot-assistant/dataset/embeddings/faiss_index.bin",
        metadata_path: str = "/home/zaki/Projects/junction/junction-ai/chatbot-assistant/dataset/embedding.json",
    ):
        self.model: Optional[SentenceTransformer] = None
        self.index: Optional[faiss.Index] = None
        self.metadata: Optional[List[Dict]] = None
        self.index_path = index_path
        self.metadata_path = metadata_path

        # Configure Google Generative AI
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.llm = genai.GenerativeModel("gemini-1.5-flash-latest")

        # Language detection patterns
        self.arabic_pattern = re.compile(
            r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]"
        )
        self.french_pattern = re.compile(r"[àâäéèêëïîôöùûüÿç]", re.IGNORECASE)

        # Ensure directories exist
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        os.makedirs(os.path.dirname(metadata_path), exist_ok=True)

    def _load_model(self):
        """Lazy load the sentence transformer model"""
        if self.model is None:
            print("Loading multilingual sentence transformer model...")
            self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    def _load_index(self):
        """Lazy load the FAISS index"""
        if self.index is None:
            print("Loading FAISS index...")
            if not os.path.exists(self.index_path):
                raise FileNotFoundError(f"FAISS index not found at {self.index_path}")
            self.index = faiss.read_index(self.index_path)

    def _load_metadata(self):
        """Lazy load the metadata"""
        if self.metadata is None:
            print("Loading metadata...")
            if not os.path.exists(self.metadata_path):
                raise FileNotFoundError(f"Metadata not found at {self.metadata_path}")
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

    def _cleanup_after_embedding(self):
        """Clean up model after embedding to free memory"""
        if self.model is not None:
            del self.model
            self.model = None
            gc.collect()

    def detect_language(self, text: str) -> str:
        """Detect language of input text"""
        text_clean = text.strip()

        if self.arabic_pattern.search(text_clean):
            return "ar"

        if self.french_pattern.search(text_clean):
            return "fr"

        french_keywords = [
            "comment",
            "où",
            "quand",
            "pourquoi",
            "vidéo",
            "sacrifice",
            "mouton",
        ]
        if any(keyword in text_clean.lower() for keyword in french_keywords):
            return "fr"

        arabic_keywords = ["كيف", "أين", "متى", "لماذا", "فيديو", "ذبيحة", "خروف"]
        if any(keyword in text_clean for keyword in arabic_keywords):
            return "ar"

        return "en"

    def search_knowledge_base(self, query: str, k: int = 3) -> List[Dict]:
        """Search the knowledge base for relevant Q&A pairs"""
        try:
            self._load_model()
            self._load_index()
            self._load_metadata()

            query_embedding = self.model.encode([query])

            self._cleanup_after_embedding()

            D, I = self.index.search(np.array(query_embedding).astype(np.float32), k)

            retrieved_items = []
            for i, idx in enumerate(I[0]):
                if idx < len(self.metadata):
                    item = self.metadata[idx].copy()
                    item["score"] = float(D[0][i])
                    retrieved_items.append(item)

            return retrieved_items

        except Exception as e:
            print(f"Error in search: {str(e)}")
            return []

    def generate_response(
        self, query: str, context_items: List[Dict], detected_language: str
    ) -> str:
        """Generate response using LLM with context"""
        context_parts = []
        for item in context_items:
            context_parts.append(f"Q: {item['question']}\nA: {item['answer']}")

        context = "\n\n".join(context_parts) or "No relevant context found."

        if detected_language == "ar":
            prompt = f"""
أنت مساعد ذكي لمنصة التحقق من مقاطع فيديو ذبح الأضاحي.
استخدم المعلومات التالية من قاعدة المعرفة لتقديم إجابة مفيدة ومهذبة وودية.

--- السياق ---
{context}
--- نهاية السياق ---

الآن أجب على هذا السؤال كما لو كنت تتحدث في محادثة مهذبة ومحترمة:
{query}

التعليمات:
- استخدم معلومات السياق لتقديم إجابات دقيقة
- كن ودودًا ومهذبًا في الحديث
- إذا لم يكن السؤال مغطى في السياق، قل ذلك بأدب واعرض المساعدة في مواضيع أخرى
- أجب باللغة العربية
- لا تتجاوز 500 حرف في الإجابة
"""
        elif detected_language == "fr":
            prompt = f"""
Vous êtes un assistant IA pour la plateforme de validation des vidéos de sacrifice de moutons.
Utilisez les informations suivantes de la base de connaissances pour fournir une réponse utile, polie et amicale.

--- CONTEXTE ---
{context}
--- FIN DU CONTEXTE ---

Maintenant, répondez à cette question comme si vous aviez une conversation respectueuse et décontractée:
{query}

Instructions:
- Utilisez les informations du contexte pour fournir des réponses précises
- Soyez conversationnel et amical
- Si la question n'est pas couverte dans le contexte, dites-le poliment et offrez d'aider sur d'autres sujets
- Répondez en français
- Ne dépassez pas 500 caractères dans la réponse
"""
        else:
            prompt = f"""
You're an AI assistant for the sheep sacrifice video validation platform.
Use the following information from the knowledge base to provide a helpful, polite, and friendly response.

--- CONTEXT ---
{context}
--- END CONTEXT ---

Now answer this question as if you're having a casual, respectful conversation:
{query}

Instructions:
- Use the context information to provide accurate answers
- Be conversational and friendly
- If the question is not covered in the context, politely say so and offer to help with other topics
- Respond in English
- Do not exceed 500 characters in the response
"""

        try:
            # Generate response using Gemini
            response = self.llm.generate_content(prompt)
            return response.text[:500]  # Enforce 500-character limit
        except Exception as e:
            # Fallback responses
            fallback_responses = {
                "ar": "أعتذر، حدث خطأ في معالجة سؤالك. يرجى المحاولة مرة أخرى.",
                "fr": "Désolé, une erreur s'est produite lors du traitement de votre question. Veuillez réessayer.",
                "en": "Sorry, an error occurred while processing your question. Please try again.",
            }
            return fallback_responses.get(detected_language, fallback_responses["en"])[
                :500
            ]

    def answer_question(self, query: str, k: int = 3) -> Dict[str, str]:
        """Main method to answer user questions"""
        try:
            detected_language = self.detect_language(query)

            context_items = self.search_knowledge_base(query, k)

            response = self.generate_response(query, context_items, detected_language)

            return {
                "query": query,
                "response": response,
                "language": detected_language,
                "context_items": len(context_items),
                "top_score": context_items[0]["score"] if context_items else 0.0,
            }

        except FileNotFoundError as e:
            return {
                "query": query,
                "response": f"Error: Required files not found. Please ensure {self.index_path} and {self.metadata_path} exist. Details: {str(e)}",
                "language": "en",
                "context_items": 0,
                "top_score": 0.0,
            }
        except Exception as e:
            return {
                "query": query,
                "response": f"Error processing your question: {str(e)}",
                "language": "en",
                "context_items": 0,
                "top_score": 0.0,
            }

    def simulate_chat(self):
        """Simulate an interactive chat in the terminal"""
        print("Welcome to the Sheep Sacrifice Validation Chatbot!")
        print("Type your question (Arabic, French, or English) or 'quit' to exit.")
        print("-" * 50)

        while True:
            query = input("You: ")
            if query.lower() == "quit":
                print("Goodbye!")
                break

            result = self.answer_question(query)
            print(f"Bot ({result['language']}): {result['response']}")
            print(
                f"(Context items found: {result['context_items']}, Top score: {
                    result['top_score']:.4f})"
            )
            print("-" * 50)


if __name__ == "__main__":
    try:
        chatbot = SacrificeValidationChatbot()
        chatbot.simulate_chat()

    except Exception as e:
        print(f"Error initializing chatbot: {str(e)}")
        print("Make sure you have:")
        print(
            "1. Run the embedding processor first to generate faiss_index.bin and embedding.json"
        )
        print("2. Set GOOGLE_API_KEY in your .env file")
        print(
            "3. Install required packages: pip install sentence-transformers faiss-cpu google-generativeai python-dotenv numpy"
        )
