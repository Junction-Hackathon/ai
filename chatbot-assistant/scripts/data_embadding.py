import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import os

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
BASE_DIR = "/home/zaki/Projects/junction/junction-ai/chatbot-assistant"
INPUT_JSON_PATH = os.path.join(BASE_DIR, "dataset", "context.json")
OUTPUT_JSON_PATH = os.path.join(BASE_DIR, "dataset", "embedding.json")
EMBEDDINGS_DIR = os.path.join(BASE_DIR, "dataset", "embeddings")

os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

try:
    model = SentenceTransformer(MODEL_NAME)
    print("Model loaded successfully")

    with open(INPUT_JSON_PATH, "r", encoding="utf-8") as f:
        knowledge_base = json.load(f)["knowledge_base"]

    texts = []
    metadata = []
    for lang in knowledge_base:
        for item in knowledge_base[lang]:
            texts.append(item["question"])
            metadata.append(
                {
                    "language": lang,
                    "question": item["question"],
                    "answer": item["answer"],
                    "category": item["category"],
                }
            )

    embeddings = model.encode(texts, show_progress_bar=True)

    data_with_embedding = []
    for item, vector in zip(metadata, embeddings):
        data_with_embedding.append(
            {
                "language": item["language"],
                "question": item["question"],
                "answer": item["answer"],
                "category": item["category"],
                "embedding": vector.tolist(),
            }
        )

    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data_with_embedding, f, indent=2, ensure_ascii=False)
    print(f"Embeddings saved to {OUTPUT_JSON_PATH}")

    embedding_array = np.array(
        [item["embedding"] for item in data_with_embedding], dtype="float32"
    )

    dimension = embedding_array.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embedding_array)

    faiss_index_path = os.path.join(EMBEDDINGS_DIR, "faiss_index.bin")
    numpy_embeddings_path = os.path.join(EMBEDDINGS_DIR, "embeddings.npy")
    faiss.write_index(index, faiss_index_path)
    np.save(numpy_embeddings_path, embedding_array)

    print(f"FAISS index saved to {faiss_index_path}")
    print(f"NumPy embeddings saved to {numpy_embeddings_path}")

except FileNotFoundError as e:
    print(f"File error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

