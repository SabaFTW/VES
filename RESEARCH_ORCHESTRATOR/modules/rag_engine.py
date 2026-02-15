# modules/rag_engine.py

import os
import uuid
import glob
from typing import List, Dict, Optional
import logging

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

def load_text_file(path: str) -> str:
    """
    Load text content from a file.
    """
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        logger.warning(f"Could not read file {path}: {e}")
        return ""


def simple_chunk(text: str, max_chars: int = 1200) -> List[str]:
    """
    Very simple character-based chunking.
    Good enough for first version.
    """
    chunks = []
    text = text.strip()
    while text:
        chunk = text[:max_chars]
        chunks.append(chunk)
        text = text[max_chars:]
    return chunks


def build_rag_index(root_dir: str,
                    file_types: List[str],
                    persist_dir: str,
                    embedding_model_name: str = "all-MiniLM-L6-v2",
                    collection_name: str = "constellation_docs") -> None:
    """
    Build or rebuild a persistent Chroma index from local files.
    """
    os.makedirs(persist_dir, exist_ok=True)

    print(f"[RAG] Initializing Chroma at: {persist_dir}")
    client = chromadb.PersistentClient(path=persist_dir, settings=Settings())
    collection = client.get_or_create_collection(name=collection_name)

    print(f"[RAG] Loading embedding model: {embedding_model_name}")
    try:
        model = SentenceTransformer(embedding_model_name)
    except Exception as e:
        logger.error(f"Could not load embedding model {embedding_model_name}: {e}")
        raise

    # Collect files
    patterns = []
    for ext in file_types:
        patterns.append(os.path.join(root_dir, f"**/*.{ext}"))

    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern, recursive=True))

    print(f"[RAG] Found {len(files)} files to index.")

    documents = []
    metadatas = []
    ids = []

    for path in files:
        text = load_text_file(path)
        if not text.strip():
            continue

        chunks = simple_chunk(text)
        for idx, chunk in enumerate(chunks):
            if len(chunk.strip()) < 10:  # Skip very short chunks
                continue
            doc_id = str(uuid.uuid4())
            documents.append(chunk)
            metadatas.append({"source": path, "chunk": idx, "type": "local"})
            ids.append(doc_id)

    if not documents:
        print("[RAG] No documents to index.")
        return

    print(f"[RAG] Encoding {len(documents)} chunks...")
    try:
        embeddings = model.encode(documents).tolist()
    except Exception as e:
        logger.error(f"Error encoding documents: {e}")
        raise

    print("[RAG] Inserting into Chroma collection...")
    try:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )
    except Exception as e:
        logger.error(f"Error adding documents to Chroma: {e}")
        raise

    print("[RAG] Index build complete.")


def query_rag(question: str,
              persist_dir: str,
              embedding_model_name: str = "all-MiniLM-L6-v2",
              collection_name: str = "constellation_docs",
              n_results: int = 10) -> List[Dict]:
    """
    Query the RAG index for semantically relevant chunks.
    """
    try:
        client = chromadb.PersistentClient(path=persist_dir, settings=Settings())
        collection = client.get_or_create_collection(name=collection_name)
    except Exception as e:
        logger.error(f"Could not access Chroma collection: {e}")
        return []

    try:
        model = SentenceTransformer(embedding_model_name)
        query_emb = model.encode([question]).tolist()
    except Exception as e:
        logger.error(f"Could not encode query: {e}")
        return []

    try:
        result = collection.query(
            query_embeddings=query_emb,
            n_results=n_results
        )
    except Exception as e:
        logger.error(f"Error querying Chroma: {e}")
        return []

    hits = []
    # result["documents"] is list-of-lists
    docs = result.get("documents", [[]])[0] if result.get("documents") else []
    metas = result.get("metadatas", [[]])[0] if result.get("metadatas") else []

    for doc, meta in zip(docs, metas):
        hits.append({
            "file": meta.get("source", "Unknown"),
            "line": meta.get("chunk", "Unknown"),
            "content": doc,
            "source": "rag",
            "type": meta.get("type", "local")
        })

    return hits