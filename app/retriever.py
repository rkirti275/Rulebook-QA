import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("../data/rulebook.index")

with open("../data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)


def search(query, top_k=5):

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        chunk = chunks[idx]

        results.append({
            "score": float(score),
            "source": chunk["source"],
            "section": chunk["section"],
            "text": chunk["text"]
        })

    return results


if __name__ == "__main__":

    question = input("\nEnter your question: ")

    results = search(question)

    print("\n" + "=" * 70)
    print("RETRIEVED RESULTS")
    print("=" * 70)

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")
        print(f"Similarity Score: {result['score']:.4f}")
        print(f"Source: {result['source']}")
        print(f"Section: {result['section']}")

        print("\nPassage:")
        print(result["text"][:500])

        print("-" * 70)