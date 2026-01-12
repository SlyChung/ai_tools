# AI Tools

A Python library providing **working memory infrastructure for AI agents**. Enables multi-agent systems to maintain persistent, structured memory through "chunks" - hierarchical data structures that agents can read, modify, and persist.

**Version**: 0.1.0
**Status**: MVP (Minimum Viable Product)
**Python**: 3.10+

## Features

- **Memory Chunk Architecture**: Hierarchical, serializable memory structures for agent state
- **Multi-Agent Support**: Designed for orchestrators coordinating specialized sub-agents
- **Standardized Tool Interface**: Consistent response format across all operations
- **Multi-Channel Logging**: Six specialized loggers for different concerns
- **Function Versioning**: Semantic versioning decorator for API stability
- **Obsidian Integration**: Vault management tools for knowledge base operations

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai_tools

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

## Quick Start

```python
from ai_tools.working_memory.sub_agent.note_writer.note_writer_memory import NoteWriterMemory

# Initialize the note writer memory
memory = NoteWriterMemory()

# Load a note
result = memory.load_note("path/to/note.md")

# Execute a tool
result = memory.execute_tool("write_note", {"content": "# My Note\nContent here..."})

# Get the current state as an envelope
state = memory.envelope()
```

## Project Structure

```
src/ai_tools/
├── general_tools/           # Reusable utilities
│   ├── file_management.py   # File I/O operations
│   ├── obsidian.py          # Obsidian vault integration (v1)
│   └── obsidian_v2.py       # Obsidian vault integration (v2)
│
├── utilities/               # Core infrastructure
│   ├── config.py            # Configuration with dot-path access
│   ├── logger.py            # Multi-channel logging system
│   ├── decorators.py        # @version("X.Y.Z") decorator
│   └── tool_envelope.py     # Standardized tool I/O wrapper
│
└── working_memory/          # Core memory architecture
    ├── Memory.py            # Abstract base class
    ├── memoryChunk.py       # Base MemoryChunk class
    ├── task.py              # Task memory chunk
    ├── notepad.py           # Notepad memory chunk
    ├── compiler.py          # Memory compilation utilities
    │
    ├── orchestrator/
    │   └── planMemory.py    # Plan tracking memory
    │
    └── sub_agent/
        ├── workingMemory.py       # Base sub-agent working memory
        ├── note_writer/           # Note writing agent
        │   ├── note_v3.py         # Current note implementation
        │   └── note_writer_memory.py
        └── vault_manager/         # Vault management agent
            ├── vault.py
            ├── file.py
            └── vault_manager_memory.py
```

## Architecture

### Memory Chunk Hierarchy

```
Memory (abstract base)
└── MemoryChunk (base chunk)
    ├── Task
    ├── Notepad
    └── WorkingMemory
        ├── NoteWriterMemory
        └── VaultManagerMemory
```

Each chunk implements the standard interface:
- `load()` - Load state from persistence
- `save()` - Save state to persistence
- `envelope()` - Return current state as dictionary
- `execute_tool()` - Execute a named tool with arguments
- `refresh()` - Update internal state

### Standardized Response Format

All tool functions return a consistent structure:

```python
{
    "status": bool,        # Success/failure
    "data": {...},         # Result data
    "message": str,        # Human-readable message
    "citations": [...],    # Optional source references
    "artifacts": [...]     # Optional generated artifacts
}
```

### Configuration

Access configuration with dot-path notation:

```python
from ai_tools.utilities.config import config

# Get nested values
log_level = config.get("logging.log_format.app.level")

# With type casting and defaults
debug = config.get("debug", cast_type=bool, default=False)
```

### Logging

Six specialized loggers configured in `config.json`:

| Logger | Purpose |
|--------|---------|
| `app` | General application events |
| `error` | Errors only |
| `api` | API interactions |
| `vault` | Vault operations |
| `technical` | Debug/technical details |
| `database` | Database operations |

### Function Versioning

Use the `@version` decorator for semantic versioning:

```python
from ai_tools.utilities.decorators import version

@version("1.0.0")
def my_function():
    pass
```

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **AI SDKs** | Anthropic, OpenAI, llama-cpp-python |
| **Data Validation** | Pydantic |
| **Database** | SQLAlchemy 2.0, Alembic (prepared for future use) |
| **Configuration** | PyYAML, Jinja2 |
| **Utilities** | tiktoken, diskcache |
| **Testing** | pytest, pytest-cov |

## Running Tests

```bash
# Run all tests
pytest tests/

# Skip stub tests (unimplemented features)
pytest tests/ -m "not stub"

# Run with coverage
pytest tests/ --cov=src/ai_tools

# Run only MVP tests
pytest tests/ -m "mvp"
```

## Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| **Utilities** | | |
| Config | 100% | Fully implemented |
| Logger | 100% | Fully implemented |
| Decorators | 100% | Versioning complete |
| ToolEnvelope | 100% | Tool wrapping complete |
| File Management | 90% | Mostly complete |
| **Working Memory** | | |
| Memory Base | 30% | 3 methods are stubs |
| MemoryChunk Base | 10% | 4 core methods are stubs |
| Task | 0% | Inherits stubs |
| Notepad | 0% | All 11 methods are stubs |
| NoteV3 | 70% | MVP implementation complete |
| NoteWriterMemory | 80% | 1 stub method |
| VaultManagerMemory | 0% | Empty file |
| PlanMemory | 5% | 1 stub method |
| Compiler | 0% | Stub function |

---

## Stubs and Unimplemented Features

The following features are defined but not yet implemented. They exist as method stubs with `pass` statements or placeholder return values.

### Core Memory Classes

#### Memory.py (Abstract Base)
| Method | Line | Description |
|--------|------|-------------|
| `load()` | 60 | Load memory state from persistence |
| `open_memory_chunk()` | 73 | Open/create a memory chunk |
| `refresh_memory()` | 154 | Refresh memory state from source |

#### memoryChunk.py (Base Class)
| Method | Line | Description |
|--------|------|-------------|
| `load()` | 47 | Load chunk state |
| `save()` | 58 | Save chunk state |
| `envelope()` | 69 | Return state dictionary |
| `execute_tool()` | 83 | Execute named tool |

#### notepad.py (Scratch Pad)
| Method | Line | Description |
|--------|------|-------------|
| `load()` | 41 | Load notepad state |
| `save()` | 49 | Save notepad state |
| `delete()` | 57 | Delete notepad |
| `close()` | 65 | Close notepad |
| `refresh()` | 73 | Refresh notepad state |
| `execute_tool()` | 84 | Execute notepad tool |
| `envelope()` | 95 | Return notepad state |
| `add_note()` | 108 | Add a note entry |
| `delete_note()` | 119 | Delete a note entry |
| `edit_note()` | 130 | Edit a note entry |
| `toggle_note_status()` | 141 | Toggle note completion |

#### task.py
All methods inherited from MemoryChunk are stubs.

#### compiler.py
| Function | Line | Description |
|----------|------|-------------|
| `compile_working_memory()` | 25 | Transform working memory to plan memory |

### Sub-Agent Memory

#### note_v3.py (Note Writer)
| Method | Line | Description |
|--------|------|-------------|
| `build_note()` | 260-269 | Build note tree structure |
| `parse_note()` | 272-283 | Parse markdown into tree |
| `add_element()` | 392 | Add element to note tree |
| `edit_element()` | 302-317 | Edit element in note tree |
| `delete_element()` | 320-333 | Delete element from note tree |

#### note_writer_memory.py
| Method | Line | Description |
|----------|------|-------------|
| `finish_payload()` | 76 | Generate completion payload |

#### vault_manager_memory.py
**Entire file is empty** - Vault manager memory not yet implemented.

### Orchestrator

#### planMemory.py
| Method | Line | Description |
|--------|------|-------------|
| `add_plan()` | 46 | Add a new plan to track |

### Unintegrated Features

#### section.py (in `Not Implemented/` directory)
A complete hierarchical section structure implementation exists but is not yet integrated:
- Supports recursive subsections
- Methods: `add_subsection()`, `remove_subsection()`, `find()`, `to_dict()`, `from_dict()`
- Status: Complete but awaiting integration

---

## Development

### Git Workflow

This repo uses an **integration-branch per subagent** workflow:

- `main`: Stable, releasable code only
- `<subagent>`: Integration branch for a workstream (e.g., `NoteWriter`)
- Feature branches: Created from integration branch
  - `feature/<prefix>-<name>`
  - `fix/<prefix>-<name>`
  - `chore/<prefix>-<name>`

**Never develop directly on `main`.**

### File Conventions

- All paths relative to `PROJECT_ROOT`
- Deprecated code in `deprecated/` directories
- Notes stored as Markdown files
- Memory chunks are serializable to dictionaries

## License

[License information here]

## Contributing

[Contributing guidelines here]
