import sys
from pathlib import Path

# Add src/ to the Python path so we can import sources, tools, etc.
sys.path.append(str(Path(__file__).resolve().parent / "src"))

import ai_tools.general_tools.file_management as fm

#print(fm.describe_module(fm))

# post fm.describe_module(fm) to the a text file
with open("file_management.txt", "w") as f:
    f.write(fm.describe_module(fm))