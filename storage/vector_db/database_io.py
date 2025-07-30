import pickle, json
import faiss  # type: ignore
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple
from .embedding import EmbeddingModel

def save_database(index: faiss.IndexFlatIP, chunks: List[str], metadata: List[Dict[str, Any]], model: EmbeddingModel, db_path: str) -> None:
    Path(db_path).mkdir(exist_ok=True)

    faiss.write_index(index, f"{db_path}/faiss_index.bin")  # type: ignore

    with open(f"{db_path}/chunks.pkl", 'wb') as f:
        pickle.dump(chunks, f)
    with open(f"{db_path}/metadata.pkl", 'wb') as f:
        pickle.dump(metadata, f)

    config: Dict[str, Any] = {
        "model_name": model.model_class(),
        "embedding_dim": model.embedding_dim(),
        "num_chunks": len(chunks),
        "created_at": datetime.now().isoformat()
    }
    with open(f"{db_path}/config.json", 'w') as f:
        json.dump(config, f, indent=2)

def load_database(db_path: str) -> Tuple[Any, List[str], List[Dict[str, Any]]]:
    index = faiss.read_index(f"{db_path}/faiss_index.bin")  # type: ignore

    with open(f"{db_path}/chunks.pkl", 'rb') as f:
        chunks: List[str] = pickle.load(f)
    with open(f"{db_path}/metadata.pkl", 'rb') as f:
        metadata: List[Dict[str, Any]] = pickle.load(f)

    return index, chunks, metadata  # type: ignore