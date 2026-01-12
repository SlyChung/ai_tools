# CLAUDE.md - AI Tools Project Guide

## What This Project Is

A Python library providing working memory infrastructure for AI agents. Enables multi-agent systems to maintain persistent, structured memory through "chunks" - hierarchical data structures that agents can read, modify, and persist.

**Current Status**: MVP (Minimum Viable Project) on branch `NoteWriter`

## Tech Stack

- **Python**: 3.10+
- **AI SDKs**: Anthropic (`anthropic`), OpenAI (`openai`), Local LLMs (`llama-cpp-python`)
- **Data**: Pydantic for validation, SQLAlchemy/Alembic for future DB support
- **Utilities**: PyYAML, Jinja2, tiktoken, diskcache

## CRITICAL: Git Workflow Requirements

This repo uses an **integration-branch per subagent** workflow.

## Branch model

- `main` (or `master`): stable, releasable code only.
- `<subagent>` integration branch: staging branch for a single subagent workstream.
  - Example: `notewriter`
- Short-lived work branches: created **from the integration branch**, then merged back into it.
  - `feature/nw-<short-kebab>`
  - `fix/nw-<short-kebab>`
  - `chore/nw-<short-kebab>`

**Policy:** Never develop directly on `main`. Prefer not to develop directly on the integration branch either—treat it like a mini-`main`.

**IMPORTANT**: You MUST follow the Git workflow for all changes:

1. **ALWAYS create a feature branch BEFORE making changes**
    '''bash
    git checkout -b feature/[feature-name] # or fix/[bug-name]
    '''

2. **Commit changes REGULARLY during development**
    - After completing each major step
    - When switching between different files/features
    - Before running build tests
    - Use meaningful commit messages with [Type] prefix

3. **NEVER work directly on main branch**
    - All changes must go through feature branches

## Project Structure

```
src/ai_tools/
├── general_tools/           # Reusable utilities
│   ├── file_management.py   # File I/O operations
│   └── obsidian.py/v2.py    # Obsidian vault integration
│
├── utilities/               # Core infrastructure
│   ├── config.py            # Configuration (dot-path access)
│   ├── logger.py            # Multi-channel logging (app, error, api, vault, technical, database)
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
    └── sub_agent/           # Specialized agent memory
        ├── workingMemory.py       # Base sub-agent working memory
        ├── note_writer/           # Note writing agent (note_v3.py is current)
        └── vault_manager/         # Vault management agent
```

## Build & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .

# Run entry point
python main.py
```

## Key Patterns

### Memory Chunk Hierarchy

```
Memory (abstract)
└── MemoryChunk
    ├── Task
    ├── Notepad
    └── WorkingMemory
        ├── NoteWriterMemory
        └── VaultManagerMemory
```

Each chunk implements: `load()`, `save()`, `envelope()`, `execute_tool()`, `refresh()`

### Standardized Response Format

All functions return:
```python
{
    "status": bool,        # Success/failure
    "data": {...},         # Result data
    "message": str,        # Human-readable message
    "citations": [...],    # Optional references
    "artifacts": [...]     # Optional artifacts
}
```

### Function Versioning

```python
@version("1.0.0")
def my_function():
    pass
```

### Configuration Access

```python
config.get("logging.log_format.app.level")
config.get("key", cast_type=bool)
```

## Logging

Six specialized loggers configured in `config.json`:
- `app` - General application
- `error` - Errors only
- `api` - API interactions
- `vault` - Vault operations
- `technical` - Debug/technical
- `database` - DB operations

## File Conventions

- All paths relative to `PROJECT_ROOT` (cwd)
- Deprecated code kept in `deprecated/` directories
- Notes stored as Markdown files
- Memory chunks are serializable to dictionaries

## Important Files

| File | Purpose |
|------|---------|
| `config.json` | Logging configuration |
| `requirements.txt` | Python dependencies |
| `pyproject.toml` | Package metadata (v0.1.0) |
| `src/ai_tools/general_tools/file_management.py` | Core file I/O (876 lines) |
| `src/ai_tools/working_memory/sub_agent/note_writer/note_v3.py` | Current note implementation |

## Development Notes

- No test suite yet - MVP phase
- Active development on `NoteWriter` branch
- Many methods are stubs awaiting implementation
- Uses file system storage; SQLAlchemy prepared for future DB use
