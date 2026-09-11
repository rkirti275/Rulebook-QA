import os
import json
import numpy as np
import faiss

from embeddings import create_embeddings


chunks, embeddings = create_embeddings()

embeddings = np.array(embeddings).astype("float32")

faiss.normalize_L2(embeddings)

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

os.makedirs("../data", exist_ok=True)

faiss.write_index(index, "../data/rulebook.index")

with open("../data/chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)

print("\nFAISS vector store created successfully!")
print(f"Total vectors: {index.ntotal}")
print(f"Vector dimension: {dimension}")
print("Saved: data/rulebook.index")
print("Saved: data/chunks.json")