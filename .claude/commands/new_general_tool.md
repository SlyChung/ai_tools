````md
# @new_general_tool.md

## Usage
`@new_general_tool.md <TOOL_NAME>`

Examples:
- `@new_general_tool.md File Management`
- `@new_general_tool.md file_management`
- `@new_general_tool.md file-management`

## Context
- New general tool name: **$ARGUMENTS**
- Project: **Obsidian_Scribe_V4**
- Target location: `general_tools/<tool_name_snake_case>.py`
- This command creates a new module file with standard imports, loggers, and a tool-specific error type.

## Your Role
You are the **General Tools Module Generator**. You create a new Python module under `general_tools/` following the project’s conventions exactly.

## Rules (Hard Requirements)
1. Convert `$ARGUMENTS` into:
   - **snake_case** for the filename: `<tool_name_snake_case>.py`
   - **PascalCase** for the error class name: `<ToolNamePascalCase>Error`
2. Create a new file: `general_tools/<tool_name_snake_case>.py`
3. The file must contain:
   - The required imports (exactly as provided)
   - The two logger instances (exactly as provided)
   - A tool-specific error class named `<ToolNamePascalCase>Error`
4. Do not create anything else.

## Required Imports (Hard Requirement)
```py
from utilities.config import PROJECT_ROOT
from utilities.logger import Logger
from utilities.decorators import version
````

## Required Logger Setup (Hard Requirement)

```py
error_logger = Logger("error")
technical_logger = Logger("technical")
```

## Required Error Class (Hard Requirement)

* Name: `<ToolNamePascalCase>Error`
* Body must match this template exactly, with only the class name changing:

```py
class <ToolNamePascalCase>Error(Exception):
    """
    Exception raised for errors in the <tool_name_snake_case> tool.
    """
    pass
```

## Process

1. Resolve `<tool_name_snake_case>` from `$ARGUMENTS`:

   * replace spaces/hyphens with `_`
   * lowercase
   * collapse multiple `_`
   * trim leading/trailing `_`
2. Resolve `<ToolNamePascalCase>` from `$ARGUMENTS`:

   * split on spaces/hyphens/underscores
   * capitalize each token
   * join with no separator
3. Create `general_tools/<tool_name_snake_case>.py` with the required content.
4. Verify the file exists and print its contents.

## Commands to Run

Use these commands (or equivalent) to perform the work:

```bash
# 1) Convert the provided name to snake_case + PascalCase manually and set them here:
TOOL_NAME_SNAKE="<tool_name_snake_case>"
TOOL_NAME_PASCAL="<ToolNamePascalCase>"

# 2) Create the new module with required content
cat > "general_tools/${TOOL_NAME_SNAKE}.py" <<EOF
from utilities.config import PROJECT_ROOT
from utilities.logger import Logger
from utilities.decorators import version

error_logger = Logger("error")
technical_logger = Logger("technical")

class ${TOOL_NAME_PASCAL}Error(Exception):
    """
    Exception raised for errors in the ${TOOL_NAME_SNAKE} tool.
    """
    pass

EOF

# 3) Verify
ls -la "general_tools/${TOOL_NAME_SNAKE}.py"
sed -n '1,80p' "general_tools/${TOOL_NAME_SNAKE}.py"

## Output Format

* Print the resolved `snake_case` name.
* Print the resolved `PascalCase` name.
* Print the created file path.

