from langchain.text_splitter import RecursiveCharacterTextSplitter
from split_chunks import raw_documents
import json

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_chunks = []

for doc in raw_documents:
    chunks = splitter.split_text(doc["text"])
    for i, chunk in enumerate(chunks):
        all_chunks.append({"content": chunk, "source": doc["path"]})


with open("dataset/chunks.json", "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, ensure_ascii=False, indent=2)

print("Chunks saved.")
