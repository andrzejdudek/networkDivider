# networkDivider: Touchstone Multi-File Sub-network Extractor

---

## Features 
- **Multi-port Touchstone Support:** Load any `.sNp` file (e.g., `.s2p`, `.s4p`, `.s8p`).
- **Batch Sub-network Extraction:** Define multiple output configurations (one per line) to process in a single batch.
- **Flexible Port Syntax:** Supports 1-based port indexing with range notations (`1-4`) and comma-separated lists (`1, 2, 5`).
- **Automatic File Naming:** Automatically names generated Touchstone files based on selected ports and output port count (e.g., `filename_ports_1_2.s2p`).
- **Cross-Platform GUI:** Modern dark-themed user interface running smoothly on Windows and Linux.

---

## Prerequisites

This project is managed using [uv](https://github.com/astral-sh/uv), an extremely fast Python package and project manager.

Make sure you have `uv` installed:

### Linux / macOS
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

### Windows
powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"

---

## Installation & Setup

### Clone the repository
git clone [https://github.com/andrzejdudek/networkDivider.git]
cd networkDivider

### Sync dependencies
uv sync

### Run
uv run main.py