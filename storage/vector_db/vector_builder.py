from pathlib import Path
import json
from .chunking import chunk_document
from .embedding import EmbeddingModel
from .indexing import FaissIndex
from .database_io import save_database, load_database
from .config import (
    PARSED_DOCS_FILE,
    DB_PATH,
    MODEL_NAME,
    MAX_CHUNK_SIZE,
    TOP_K
)

def build_vector_db():
    if not Path(PARSED_DOCS_FILE).exists():
        print("❌ Parsed document file not found.")
        return

    print(f"📚 Loading {PARSED_DOCS_FILE}")
    with open(PARSED_DOCS_FILE, 'r', encoding='utf-8') as f:
        documents = json.load(f)

    all_chunks, all_metadata = [], []
    print(f"🔄 Processing {len(documents)} documents...")
    for doc in documents:
        if doc['status'] != 'success':
            continue
        filename = Path(doc['filename']).name
        content = doc.get('content', '')
        if not content:
            continue
        print(f"  📄 {filename}")
        chunks, metadata = chunk_document(content, filename, MAX_CHUNK_SIZE)
        all_chunks.extend(chunks)
        all_metadata.extend(metadata)

    print(f"📊 Chunked into {len(all_chunks)} total segments")
    model = EmbeddingModel(MODEL_NAME)
    embeddings = model.encode_chunks(all_chunks)

    indexer = FaissIndex(dim=embeddings.shape[1])
    indexer.add_embeddings(embeddings)

    save_database(indexer.index, all_chunks, all_metadata, model, DB_PATH)
    print(f"✅ Saved to {DB_PATH}/")
    return model, indexer, all_chunks, all_metadata

def test_search(model, indexer, chunks, metadata):
    queries = [
        "RMF authorization process",
        "STIG compliance requirements",
        "NIST cybersecurity framework",
    ]

    for query in queries:
        print(f"\n🔎 Query: {query}")
        query_embedding = model.encode_query(query)
        scores, indices = indexer.search(query_embedding, TOP_K)

        for i, (score, idx) in enumerate(zip(scores, indices), 1):
            preview = chunks[idx][:100]
            file = metadata[idx]['filename']
            print(f"  {i}. {file} (score: {score:.3f})")
            print(f"     {preview}...")

if __name__ == "__main__":
    model, indexer, chunks, metadata = build_vector_db()
    test_search(model, indexer, chunks, metadata)