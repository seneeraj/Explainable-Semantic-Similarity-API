import spacy
from typing import List
from collections import OrderedDict

# Load spaCy model ONCE
_nlp = spacy.load("en_core_web_sm", disable=["ner"])

# Ensure sentence boundaries exist (required for TextRank safety)
if "sentencizer" not in _nlp.pipe_names:
    _nlp.add_pipe("sentencizer")

try:
    import pytextrank
    if "textrank" not in _nlp.pipe_names:
        _nlp.add_pipe("textrank")
    TEXTRANK_AVAILABLE = True
except ImportError:
    TEXTRANK_AVAILABLE = False


def _deduplicate_preserve_order(items: List[str]) -> List[str]:
    """
    Deduplicate while preserving original order.
    """
    return list(OrderedDict.fromkeys(items))


def extract_key_concepts(text: str, top_n: int = 30) -> List[str]:
    """
    Extract explainable, audit-safe key concepts from source document.

    Strategy (Path-A compliant):
    1. TextRank key phrases (if available)
    2. Noun chunks
    3. Verb–object phrases (action-based concepts)

    No LLMs. No synonyms. Deterministic only.
    """

    if not text or not text.strip():
        return []

    doc = _nlp(text)

    concepts: List[str] = []

    # ------------------------------------------------------------------
    # 1️⃣ TextRank phrases (high-signal noun phrases)
    # ------------------------------------------------------------------
    if TEXTRANK_AVAILABLE:
        for phrase in doc._.phrases:
            phrase_text = phrase.text.strip().lower()
            if 2 <= len(phrase_text.split()) <= 6:
                concepts.append(phrase_text)

    # ------------------------------------------------------------------
    # 2️⃣ Noun chunks (entity & concept coverage)
    # ------------------------------------------------------------------
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.strip().lower()
        if 2 <= len(chunk_text.split()) <= 6:
            concepts.append(chunk_text)

    # ------------------------------------------------------------------
    # 3️⃣ Verb–object phrases (CRITICAL for recall)
    #     Examples:
    #       "ensure compliance"
    #       "reduce emissions"
    #       "conduct audits"
    # ------------------------------------------------------------------
    for token in doc:
        if token.pos_ == "VERB":
            # Direct object
            dobj = [child for child in token.children if child.dep_ == "dobj"]
            for obj in dobj:
                phrase = f"{token.lemma_} {obj.text}".lower()
                if 2 <= len(phrase.split()) <= 6:
                    concepts.append(phrase)

            # Prepositional object (e.g., "comply with regulations")
            for prep in [c for c in token.children if c.dep_ == "prep"]:
                pobj = [c for c in prep.children if c.dep_ == "pobj"]
                for obj in pobj:
                    phrase = f"{token.lemma_} {prep.text} {obj.text}".lower()
                    if 2 <= len(phrase.split()) <= 6:
                        concepts.append(phrase)

    # ------------------------------------------------------------------
    # 4️⃣ Cleanup & selection
    # ------------------------------------------------------------------
    concepts = _deduplicate_preserve_order(concepts)

    return concepts[:top_n]
