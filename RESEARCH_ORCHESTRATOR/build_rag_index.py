# build_rag_index.py

import yaml
from modules.rag_engine import build_rag_index

if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    search_cfg = config["search"]
    rag_cfg = config["rag"]

    build_rag_index(
        root_dir=search_cfg["local_dir"],
        file_types=search_cfg["file_types"],
        persist_dir=rag_cfg["persist_dir"],
        embedding_model_name=rag_cfg["embedding_model"],
        collection_name=rag_cfg["collection_name"]
    )