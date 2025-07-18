import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-minilm-l3-v2")

with open("./dataset/chunks.json", "r", encoding="utf-8") as f:
    data = json.load(f)

batch_size = 100
all_embeddings = []

for i in range(0, len(data), batch_size):
    batch = data[i: i + batch_size]
    texts = [item["content"] for item in batch]
    embeddings = model.encode(texts, show_progress_bar=True)
    all_embeddings.extend(embeddings)

    import gc

    gc.collect()

embeddings = np.array(all_embeddings, dtype="float32")
metadata = [{"source": item["source"], "content": item["content"]}
            for item in data]

faiss.normalize_L2(embeddings)
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

faiss.write_index(index, "./dataset/faiss.index")
with open("./dataset/metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print("FAISS index and metadata saved with memory optimization.")
