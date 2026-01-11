"""
File management tools for the scribe.

TODO: Need to fix the descriptions since these functions are not in direct use by agents.
"""
import os
import sys
import re
import shutil

from utilities.config import PROJECT_ROOT
from utilities.logger import Logger
from utilities.decorators import version

error_logger = Logger("error")
technical_logger = Logger("technical")

from pathlib import Path
import inspect
import json

# Deprecated
def describe_module(module):
    """
    Describe a module
    """
    info = {"name": module.__name__, "description": inspect.getdoc(module) or "", "functions": []}
    for name, func in inspect.getmembers(module, inspect.isfunction):
        sig = inspect.signature(func)
        info["functions"].append({
            "name": name,
            "description": inspect.getdoc(func) or "",
            "parameters": [
                {"name": p.name, "type": str(p.annotation), "default": str(p.default) if p.default is not inspect._empty else None}
                for p in sig.parameters.values()
            ],
            "returns": str(sig.return_annotation) if sig.return_annotation is not inspect._empty else "None"
        })
    return json.dumps(info, indent=4)

@version("1.1.0")
def create_directory(directory_path: str) -> Path:
    """
    Create a directory.

    Args:
        directory_path: Target directory path relative to PROJECT_ROOT.

    Returns:
        Path object of the created (or existing) directory.

    Raises:
        FileManagementError: On permission errors or invalid paths.

    Notes:
        Idempotent: succeeds if the directory already exists.
    """
    folder_path = PROJECT_ROOT / directory_path

    try:
        technical_logger.log_info(f"file_management.create_directory: Creating directory: {directory_path}")
        os.makedirs(folder_path, exist_ok=True)
        return folder_path
    except Exception as e:
        error_logger.log_error(f"file_management.create_directory: Error creating directory: {directory_path}: {e}")
        raise FileManagementError(f"Error creating directory: {directory_path}: {e}")

@version("1.1.0")
def create_file(file_path: str, file_name: str, overwrite: bool = False) -> Path:
    """
    Create an empty file on disk.

    Args:
        file_path: Folder path relative to PROJECT_ROOT.
        file_name: Name of the file to create.
        overwrite: If True, replace an existing file.

    Returns:
        Path object of the created file.

    Raises:
        FileManagementError: If file exists and overwrite=False, or on permission errors.

    Notes:
        Creates parent directories if they don't exist.
    """
    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name

    technical_logger.log_info(f"file_management.create_file: Creating file: {file_name}")
    try:
        folder_path.mkdir(parents=True, exist_ok=True)

        if full_path.exists() and not overwrite:
            raise FileManagementError(f"File already exists: {full_path}")

        with open(full_path, "w") as f:
            f.write("")
        return full_path
    except FileManagementError:
        raise
    except Exception as e:
        error_logger.log_error(f"file_management.create_file: Error creating file: {file_name}: {e}")
        raise FileManagementError(f"Error creating file: {file_name}: {e}")

@version("1.1.0")
def delete_file(file_path: str, file_name: str) -> None:
    """
    Delete a file.

    Args:
        file_path: Folder path relative to PROJECT_ROOT.
        file_name: Name of the file to delete.

    Returns:
        None

    Raises:
        FileManagementError: On permission errors or other OS errors.

    Notes:
        Idempotent: succeeds even if the file does not exist.
    """
    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name

    technical_logger.log_info(f"file_management.delete_file: Deleting file: {file_name}")
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
    except Exception as e:
        error_logger.log_error(f"file_management.delete_file: Error deleting file: {file_name}: {e}")
        raise FileManagementError(f"Error deleting file: {file_name}: {e}")

@version("1.1.0")
def read_file(file_path: str, file_name: str) -> str:
    """
    Read a file.

    Args:
        file_path: Folder path relative to PROJECT_ROOT.
        file_name: Name of the file to read.

    Returns:
        The file contents as a string.

    Raises:
        FileManagementError: If file does not exist or on other errors.

    Notes:
        Opens in text mode with platform default encoding.
        Best for text files; binary files may yield unreadable content.
    """
    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name

    technical_logger.log_info(f"file_management.read_file: Reading file: {file_name}")
    try:
        with open(full_path, "r") as f:
            return f.read()
    except Exception as e:
        error_logger.log_error(f"file_management.read_file: Error reading file: {file_name}: {e}")
        raise FileManagementError(f"Error reading file: {file_name}: {e}")
    
@version("1.1.0")
def write_file(file_path: str, file_name: str, content: str) -> None:
    """
    Write to a file.

    Args:
        file_path: Folder path relative to PROJECT_ROOT.
        file_name: Name of the file to write.
        content: String data to write to the file.

    Returns:
        None

    Raises:
        FileManagementError: On permission errors or other OS errors.

    Notes:
        Opens in text mode with platform default encoding.
        Overwrites (truncates) existing files; does not create parent directories.
    """
    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name

    try:
        technical_logger.log_info(f"file_management.write_file: Writing to file: {file_name}")
        with open(full_path, "w") as f:
            f.write(content)
    except Exception as e:
        error_logger.log_error(f"file_management.write_file: Error writing to file: {file_name}: {e}")
        raise FileManagementError(f"Error writing to file: {file_name}: {e}")

@version("1.1.0")
def append_file(file_path: str, file_name: str, content: str) -> None:
    """
    Append content to a file.

    Args:
        file_path: Folder path relative to PROJECT_ROOT.
        file_name: Name of the file to append to.
        content: String data to append.

    Returns:
        None

    Raises:
        FileManagementError: On permission errors or other OS errors.

    Notes:
        Creates the file if it does not exist; does NOT create parent directories.
        Not idempotent: repeated calls append repeatedly.
    """
    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name

    technical_logger.log_info(f"file_management.append_file: Appending to file: {file_name}")
    try:
        with open(full_path, "a") as f:
            f.write(content)
    except Exception as e:
        error_logger.log_error(f"file_management.append_file: Error appending to file: {file_name}: {e}")
        raise FileManagementError(f"Error appending to file: {file_name}: {e}")

@version("1.1.0")
def list_files(directory_path: str) -> list[str]:
    """
    List all files and folders in a directory.

    Args:
        directory_path: Folder path relative to PROJECT_ROOT.

    Returns:
        List of file/folder names (not full paths). Not recursive.

    Raises:
        FileManagementError: If directory does not exist or on permission errors.

    Notes:
        Includes both files and subdirectories; hidden dotfiles may be included.
        Ordering is arbitrary (not sorted).
    """
    folder_path = PROJECT_ROOT / directory_path

    technical_logger.log_info(f"file_management.list_files: Listing files in directory: {directory_path}")
    try:
        return os.listdir(folder_path)
    except Exception as e:
        error_logger.log_error(f"file_management.list_files: Error listing files in directory: {directory_path}: {e}")
        raise FileManagementError(f"Error listing files in directory: {directory_path}: {e}")

@version("1.1.0")
def list_direct_subdirectories(directory_path: str) -> list[str]:
    """
    List all subdirectories in a directory (non-recursive).

    Args:
        directory_path: Folder path relative to PROJECT_ROOT.

    Returns:
        List of subdirectory names (not full paths). First-level only.

    Raises:
        FileManagementError: If directory does not exist or on permission errors.

    Notes:
        Excludes regular files; includes symlinked directories.
        Order is not guaranteed.
    """
    folder_path = PROJECT_ROOT / directory_path

    technical_logger.log_info(f"file_management.list_direct_subdirectories: Listing directories in directory: {directory_path}")
    try:
        return [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
    except Exception as e:
        error_logger.log_error(f"file_management.list_direct_subdirectories: Error listing directories in directory: {directory_path}: {e}")
        raise FileManagementError(f"Error listing directories in directory: {directory_path}: {e}")
    
# TODO: Implement recursive listing
@version("1.1.0")
def list_all_subdirectories(directory_path: str) -> list[str]:
    """
    List all subdirectories in a directory recursively.

    Args:
        directory_path: Folder path relative to PROJECT_ROOT.

    Returns:
        List of subdirectory names. Currently delegates to list_direct_subdirectories.

    Raises:
        FileManagementError: If directory does not exist or on permission errors.

    Notes:
        TODO: Currently only returns first-level subdirectories.
    """
    return list_direct_subdirectories(directory_path)

@version("1.1.0")
def move_file(file_path: str, file_name: str, destination_path: str) -> Path:
    """
    Move a file to a destination directory.

    Args:
        file_path: Source folder path relative to PROJECT_ROOT.
        file_name: Name of the file to move.
        destination_path: Destination folder path relative to PROJECT_ROOT.

    Returns:
        Path object of the file in its new location.

    Raises:
        FileManagementError: If source does not exist or on other errors.

    Notes:
        Destination directory must already exist.
        Uses atomic rename when possible (same filesystem).
    """
    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name
    destination_folder_path = PROJECT_ROOT / destination_path
    destination_full_path = destination_folder_path / file_name

    technical_logger.log_info(f"file_management.move_file: Moving file: {file_name} to {destination_path}")
    try:
        if not os.path.exists(full_path):
            raise FileManagementError(f"Source file does not exist: {full_path}")
        shutil.move(full_path, destination_full_path)
        return destination_full_path
    except FileManagementError:
        raise
    except Exception as e:
        error_logger.log_error(f"file_management.move_file: Error moving file: {file_name} to {destination_path}: {e}")
        raise FileManagementError(f"Error moving file: {file_name} to {destination_path}: {e}")
    
@version("1.1.0")
def copy_file(file_path: str, file_name: str, destination_path: str) -> Path:
    """
    Copy a file to a destination directory.

    Args:
        file_path: Source folder path relative to PROJECT_ROOT.
        file_name: Name of the file to copy.
        destination_path: Destination folder path relative to PROJECT_ROOT.

    Returns:
        Path object of the copied file.

    Raises:
        FileManagementError: If source does not exist or on other errors.

    Notes:
        Destination directory must already exist.
        Overwrites an existing file of the same name in the destination.
    """
    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name
    destination_folder_path = PROJECT_ROOT / destination_path
    destination_full_path = destination_folder_path / file_name

    technical_logger.log_info(f"file_management.copy_file: Copying file: {file_name} to {destination_path}")
    try:
        if not os.path.exists(full_path):
            raise FileManagementError(f"Source file does not exist: {full_path}")
        shutil.copy(full_path, destination_full_path)
        return destination_full_path
    except FileManagementError:
        raise
    except Exception as e:
        error_logger.log_error(f"file_management.copy_file: Error copying file: {file_name} to {destination_path}: {e}")
        raise FileManagementError(f"Error copying file: {file_name} to {destination_path}: {e}")

@version("1.1.0")
def rename_file(file_path: str, file_name: str, new_name: str) -> Path:
    """
    Rename a file.

    Args:
        file_path: Folder path relative to PROJECT_ROOT.
        file_name: Current name of the file (with extension).
        new_name: New file name (with extension).

    Returns:
        Path object of the renamed file.

    Raises:
        FileManagementError: If source does not exist, target already exists, or on other errors.

    Notes:
        Operates only within file_path (no moves across directories).
        Not idempotent: repeating will fail after the first success.
    """
    folder_path = PROJECT_ROOT / file_path
    old_path = folder_path / file_name
    new_path = folder_path / new_name

    technical_logger.log_info(f"file_management.rename_file: Renaming file: {file_name} to {new_name}")
    try:
        if not os.path.exists(old_path):
            raise FileManagementError(f"Source file does not exist: {old_path}")
        if os.path.exists(new_path):
            raise FileManagementError(f"Target file already exists: {new_path}")
        os.rename(old_path, new_path)
        return new_path
    except FileManagementError:
        raise
    except Exception as e:
        error_logger.log_error(f"file_management.rename_file: Error renaming file: {file_name} to {new_name}: {e}")
        raise FileManagementError(f"Error renaming file: {file_name} to {new_name}: {e}")

@version("1.1.0")
def file_exists(file_path: str, file_name: str) -> bool:
    """
    Check if a file exists.

    Args:
        file_path: Folder path relative to PROJECT_ROOT.
        file_name: Name of the file to check.

    Returns:
        True if the file exists, False otherwise.

    Raises:
        FileManagementError: On permission errors or other OS errors.
    """
    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name

    technical_logger.log_info(f"file_management.file_exists: Checking if file exists: {file_name} in {file_path}")
    try:
        return os.path.exists(full_path)
    except Exception as e:
        error_logger.log_error(f"file_management.file_exists: Error checking if file exists: {file_name} in {file_path}: {e}")
        raise FileManagementError(f"Error checking if file exists: {file_name} in {file_path}: {e}")

@version("1.1.0")
def directory_exists(directory_path: str) -> bool:
    """
    Check if a directory exists.

    Args:
        directory_path: Folder path relative to PROJECT_ROOT.

    Returns:
        True if the directory exists and is a directory, False otherwise.

    Raises:
        FileManagementError: On permission errors or other OS errors.
    """
    folder_path = PROJECT_ROOT / directory_path

    technical_logger.log_info(f"file_management.directory_exists: Checking if directory exists: {directory_path}")
    try:
        return os.path.exists(folder_path) and os.path.isdir(folder_path)
    except Exception as e:
        error_logger.log_error(f"file_management.directory_exists: Error checking if directory exists: {directory_path}: {e}")
        raise FileManagementError(f"Error checking if directory exists: {directory_path}: {e}")

@version("1.0.0")
def is_valid_filename(name: str, target_os: str = "auto") -> bool:
    """
    Return False if 'name' is invalid for the target OS; True otherwise.
    target_os: 'windows' | 'mac' | 'linux' | 'auto'
    """

    _WINDOWS_FORBIDDEN_CHARS = set('\\/:*?"<>|')
    _WINDOWS_RESERVED = {
        "CON","PRN","AUX","NUL",
        *{f"COM{i}" for i in range(1,10)},
        *{f"LPT{i}" for i in range(1,10)}
    }

    if not isinstance(name, str):
        return False

    # empty, dot, dot-dot are not valid segment names anywhere
    if name in ("", ".", ".."):
        return False

    # Resolve OS target
    if target_os == "auto":
        if sys.platform.startswith("win"):
            target = "windows"
        elif sys.platform == "darwin":
            target = "mac"
        else:
            target = "linux"
    else:
        target = target_os.lower()

    # NUL byte is universally forbidden
    if "\x00" in name:
        return False

    # Per-OS checks
    if target == "windows":
        # Forbidden characters
        if any(ch in _WINDOWS_FORBIDDEN_CHARS for ch in name):
            return False
        # Control chars 0x00–0x1F
        if any(ord(ch) < 32 for ch in name):
            return False
        # Trailing space or period is invalid
        if name.endswith(" ") or name.endswith("."):
            return False
        # Reserved device names (case-insensitive), with or without extension
        base = name.split(".")[0].upper()
        if base in _WINDOWS_RESERVED:
            return False
        # Length limit (most filesystems: 255 chars for a single segment)
        if len(name) > 255:
            return False
        # Slash is already covered in forbidden chars; backslash too
        return True

    elif target == "mac":
        # macOS forbids "/" and historically ":" (block both)
        if "/" in name or ":" in name:
            return False
        # Length limit
        if len(name.encode("utf-8")) > 255:
            return False
        return True

    elif target == "linux":
        # Linux forbids "/" in a segment
        if "/" in name:
            return False
        # Length limit (bytes)
        if len(name.encode("utf-8")) > 255:
            return False
        return True

    # Unknown target
    return False

@version("1.0.0")
def find_file(file_id: str) -> list[str]:
    """
    Find a file in the file system

    Returns: [file_path, file_name]
    """
    pass
        

class FileManagementError(Exception):
    """
    Exception raised for errors in the file management tool.
    """
    pass
