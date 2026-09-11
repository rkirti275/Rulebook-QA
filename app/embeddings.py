from sentence_transformers import SentenceTransformer
from chunking import create_chunks


# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings():
    chunks = create_chunks()

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return chunks, embeddings


if __name__ == "__main__":

    chunks, embeddings = create_embeddings()

    print("\nEmbeddings created successfully!")
    print(f"Total chunks: {len(chunks)}")
    print(f"Embedding shape: {embeddings.shape}")