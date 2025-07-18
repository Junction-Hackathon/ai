from sentence_transformers import SentenceTransformer
import json


model = SentenceTransformer("all-MiniLM-L6-v2")
with open("./dataset/chunks.json", "r", encoding="utf-8") as f:
    chunked_data = json.load(f)

texts = [item["content"] for item in chunked_data]
embeddings = model.encode(texts, show_progress_bar=True)

data_with_embadding = []

for item, vector in zip(chunked_data, embeddings):
    data_with_embadding.append(
        {
            "source": item["source"],
            "content": item["content"],
            "embedding": vector.tolist(),
        }
    )

with open("./dataset/chunks.json", "w", encoding="utf-8") as f:
    json.dump(data_with_embadding, f, indent=2)
