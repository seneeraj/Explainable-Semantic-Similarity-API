import spacy
from typing import List

# Load once (important for performance)
_nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
_nlp.add_pipe("sentencizer")


def chunk_document(
    text: str,
    sentences_per_chunk: int = 4,
    overlap: int = 1
) -> List[str]:
    """
    Split document into overlapping sentence chunks.

    Example:
    sentences_per_chunk = 4
    overlap = 1

    [S1 S2 S3 S4]
             [S4 S5 S6 S7]
    """

    if not text or not text.strip():
        return []

    doc = _nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    chunks = []
    start = 0

    while start < len(sentences):
        end = start + sentences_per_chunk
        chunk = sentences[start:end]

        if chunk:
            chunks.append(" ".join(chunk))

        # Move window forward with overlap
        start = end - overlap

        if start < 0:
            start = 0

    return chunks
