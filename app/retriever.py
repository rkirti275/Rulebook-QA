import json
import math
import re
from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CHUNKS_FILE = DATA_DIR / "chunks.json"


with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)


def tokenize(text):
    return re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())


def cosine_similarity(query_words, document_words):
    query_count = Counter(query_words)
    document_count = Counter(document_words)

    common_words = set(query_count) & set(document_count)

    if not common_words:
        return 0.0

    dot_product = sum(
        query_count[word] * document_count[word]
        for word in common_words
    )

    query_magnitude = math.sqrt(
        sum(value ** 2 for value in query_count.values())
    )

    document_magnitude = math.sqrt(
        sum(value ** 2 for value in document_count.values())
    )

    if query_magnitude == 0 or document_magnitude == 0:
        return 0.0

    return dot_product / (query_magnitude * document_magnitude)


def search(query, top_k=5):

    query_words = tokenize(query)

    scored_results = []

    for chunk in chunks:

        document_words = tokenize(chunk["text"])

        score = cosine_similarity(
            query_words,
            document_words
        )

        scored_results.append({
            "score": score,
            "source": chunk["source"],
            "section": chunk["section"],
            "text": chunk["text"]
        })

    scored_results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scored_results[:top_k]


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