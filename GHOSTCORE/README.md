# Ghostcore Evidence OS V5.2

A modular forensic evidence compilation system for investigative research.

## Structure

- `bin/` - Command line interface
- `core/` - Core runtime and compiler
- `modules/` - Pluggable modules (exporters, charts, etc.)
- `templates/` - Document templates
- `cases/` - Case definition files (FCM format)
- `build/` - Output directory

## Usage

```bash
ghostcore build cases/example_case.yaml
```

## Features

- Multi-format export (PDF, DOCX)
- Modular architecture
- Identity kernel with anti-tamper protection
- Case compilation from YAML definitions
- ZIP packaging of all artifacts
- Structured logging

## FCM Format

The Forensic Case Model (FCM) defines evidence cases in YAML format with:
- Case metadata
- Document sections
- Exhibits and diagrams
- Output formats

## Modules

The system supports pluggable modules for:
- PDF export
- DOCX export
- Chart generation
- Diagram building
- Upload services
