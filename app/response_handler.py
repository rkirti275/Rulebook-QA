from app.retriever import search


# Minimum similarity required
SIMILARITY_THRESHOLD = 0.45


def check_conflict(results):
    """
    Detect known contradictions in retrieved passages.
    """

    texts = [r["text"].lower() for r in results]

    combined_text = " ".join(texts)

    # Attendance conflict
    if "75%" in combined_text and "60%" in combined_text:
        return True, "Attendance"

    # Fee conflict
    if "15 august" in combined_text and "20 august" in combined_text:
        return True, "Fee Deadline"

    # Hostel conflict
    if "9 pm" in combined_text and "10 pm" in combined_text:
        return True, "Hostel Entry"

    return False, None


def check_response(question):

    results = search(question, top_k=5)

    if not results:
        return {
            "status": "not_covered",
            "answer": "This question is not covered in the university rulebook.",
            "results": []
        }

    best_score = results[0]["score"]

    # Not covered
    if best_score < SIMILARITY_THRESHOLD:
        return {
            "status": "not_covered",
            "answer": (
                "This question is not sufficiently covered "
                "in the university rulebook."
            ),
            "results": results
        }

    # Conflict detection
    conflict, conflict_type = check_conflict(results)

    if conflict:

        return {
            "status": "conflict",
            "answer": (
                f"Conflicting provisions were found regarding "
                f"{conflict_type}. Please refer to the cited sections "
                f"or consult the competent authority."
            ),
            "results": results
        }

    # Normal answer
    best_result = results[0]

    answer = best_result["text"]

    return {
        "status": "answered",
        "answer": answer,
        "results": results
    }


if __name__ == "__main__":

    question = input("\nEnter your question: ")

    response = check_response(question)

    print("\n" + "=" * 70)
    print("STATUS:", response["status"])
    print("=" * 70)

    print("\nANSWER:")
    print(response["answer"])

    print("\nCITATIONS:")

    for i, result in enumerate(response["results"], start=1):

        print(f"\n[{i}] Source: {result['source']}")
        print(f"Similarity Score: {result['score']:.4f}")
        print("Passage:")
        print(result["text"][:300])
        print("-" * 70)