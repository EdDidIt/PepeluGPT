import pickle, json
import faiss
from pathlib import Path
from datetime import datetime

def save_database(index, chunks, metadata, model, db_path):
    Path(db_path).mkdir(exist_ok=True)

    faiss.write_index(index, f"{db_path}/faiss_index.bin")

    with open(f"{db_path}/chunks.pkl", 'wb') as f:
        pickle.dump(chunks, f)
    with open(f"{db_path}/metadata.pkl", 'wb') as f:
        pickle.dump(metadata, f)

    config = {
        "model_name": model.model_class(),
        "embedding_dim": model.embedding_dim(),
        "num_chunks": len(chunks),
        "created_at": datetime.now().isoformat()
    }
    with open(f"{db_path}/config.json", 'w') as f:
        json.dump(config, f, indent=2)

def load_database(db_path):
    index = faiss.read_index(f"{db_path}/faiss_index.bin")

    with open(f"{db_path}/chunks.pkl", 'rb') as f:
        chunks = pickle.load(f)
    with open(f"{db_path}/metadata.pkl", 'rb') as f:
        metadata = pickle.load(f)

    return index, chunks, metadata