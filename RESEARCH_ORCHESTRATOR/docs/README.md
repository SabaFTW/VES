# CONSTELLATION RESEARCH TOOLCHAIN

A local, open-source research automation stack inspired by multi-source
search, evidence chaining, and pattern recognition workflows.

## Features
- Local file search (ripgrep)
- Optional Brave API search
- Optional Google Drive API
- Pattern analysis (networks, timelines)
- Local LLM integration (Ollama, vLLM, llama.cpp)
- Forensic report generation
- RAG (Retrieval-Augmented Generation) with Chroma vector database

## Requirements
- Python 3.9+
- ripgrep
- Ollama (recommended)

## Install
```
./install.sh
```

## Setup RAG Index
To build the semantic search index:
```
python build_rag_index.py
```

## Run Research
```
python orchestrator.py --question "Your question" --keywords kw1 kw2 kw3
```

To enable web search:
```
python orchestrator.py --question "Your question" --keywords kw1 kw2 kw3 --web
```

## Project Structure
```
constellation_research/
│
├── orchestrator.py
├── config.yaml
├── install.sh
├── requirements.txt
│
├── modules/
│   ├── local_search.py
│   ├── web_search.py
│   ├── drive_search.py
│   ├── model_runner.py
│   ├── pattern_analysis.py
│   ├── report_generator.py
│   └── rag_engine.py
│
├── tools/
│   ├── hash_utils.py
│   ├── pdf_parser.py
│   ├── graph_builder.py
│   └── timeline_extractor.py
│
├── samples/
│   └── example_report.md
│
├── rag_index/          # Chroma database
└── docs/
    └── README.md
```

## Configuration
Edit `config.yaml` to customize:
- Model settings
- Search directories and file types
- Output format
- RAG settings
- API keys

## Notes
- For local LLM, install and run Ollama with your preferred model
- Web search requires Brave API key
- RAG index needs to be built before first use
- All processing happens locally for privacy