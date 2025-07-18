import glob

files = glob.glob("./dataset/**/*.txt", recursive=True)

raw_documents = []

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    raw_documents.append({"path": file, "text": text})

print(f"Loaded {len(raw_documents)} documents.")
