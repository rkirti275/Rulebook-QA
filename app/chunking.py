from pathlib import Path
import pandas as pd
import pymupdf
import re


CORPUS_DIR = Path(__file__).resolve().parent.parent / "corpus"


def read_markdown(file_path):
    return file_path.read_text(encoding="utf-8")


def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_string(index=False)


def read_pdf(file_path):
    document = pymupdf.open(file_path)

    pages = []

    for page in document:
        pages.append(page.get_text())

    document.close()

    return "\n".join(pages)


def load_documents():
    documents = []

    for file_path in CORPUS_DIR.iterdir():

        if file_path.suffix.lower() == ".md":
            text = read_markdown(file_path)

        elif file_path.suffix.lower() == ".csv":
            text = read_csv(file_path)

        elif file_path.suffix.lower() == ".pdf":
            text = read_pdf(file_path)

        else:
            continue

        documents.append({
            "source": file_path.name,
            "text": text
        })

    return documents


def find_section(text):
    """
    Chunk ke text me latest section/heading find karta hai.
    """

    section = "General"

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        # Markdown headings
        if line.startswith("#"):
            section = line.lstrip("#").strip()

        # Numbered sections like:
        # 2.1 Attendance Requirement
        # 5.3 Medical Exemption
        elif re.match(r"^\d+(\.\d+)*[\s.)-]", line):
            section = line

    return section


def chunk_text(text, chunk_size=800, overlap=100):
    """
    Document ko chhote overlapping chunks mein divide karta hai.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks():

    documents = load_documents()

    all_chunks = []

    for document in documents:

        chunks = chunk_text(document["text"])

        for number, chunk in enumerate(chunks):

            section = find_section(chunk)

            all_chunks.append({
                "source": document["source"],
                "section": section,
                "chunk_id": number,
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":

    chunks = create_chunks()

    print(f"Total chunks created: {len(chunks)}")

    print("\nFirst 3 chunks:\n")

    for chunk in chunks[:3]:

        print("----------------------------------------")
        print(f"Source: {chunk['source']}")
        print(f"Section: {chunk['section']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(chunk["text"][:500])