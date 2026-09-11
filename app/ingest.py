from pathlib import Path
import pandas as pd
import fitz  # PyMuPDF


# Project ke corpus folder ka path
CORPUS_DIR = Path(__file__).resolve().parent.parent / "corpus"


def read_markdown(file_path):
    """Read a Markdown file."""
    return file_path.read_text(encoding="utf-8")


def read_csv(file_path):
    """Read a CSV file and convert it into readable text."""
    df = pd.read_csv(file_path)

    text = df.to_string(index=False)

    return text


def read_pdf(file_path):
    """Read text from every page of a PDF."""
    document = fitz.open(file_path)

    pages = []

    for page in document:
        pages.append(page.get_text())

    document.close()

    return "\n".join(pages)


def load_corpus():
    """Read all supported files from the corpus folder."""
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

        documents.append(
            {
                "source": file_path.name,
                "text": text
            }
        )

    return documents


if __name__ == "__main__":

    documents = load_corpus()

    print(f"Total documents loaded: {len(documents)}")

    for document in documents:
        print(f"- {document['source']}")
        print(f"  Characters: {len(document['text'])}")