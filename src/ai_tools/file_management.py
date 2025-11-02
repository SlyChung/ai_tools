"""
File management tools for the scribe.
"""
import os
import shutil

from utilities.config import PROJECT_ROOT
from utilities.logger import Logger
from utilities.decorators import version

error_logger = Logger("error")
technical_logger = Logger("technical")

import inspect
import json
from pathlib import Path

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

# Deprecated
def create_directory(directory_path: str) -> dict:
    """
    Create a directory
    """

    try:
        technical_logger.log_info(f"file_management.create_directory: Creating directory: {directory_path}")
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        return {
            "success": True,
            "data": {
                "directory_path": directory_path
            },
            "message": f"Directory {directory_path} created successfully"
        }
    except Exception as e:
        error_logger.log_error(f"file_management.create_directory: Error creating directory: {directory_path}: {e}")
        return {
            "success": False,
            "data": None,
            "message": f"Error creating directory: {directory_path}: {e}"
        }

@version("1.0.0")
def create_file(file_path: str, file_name: str, overwrite: bool = False) -> dict:
    """
    Create a file
    """

    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name

    technical_logger.log_info(f"file_management.create_file: Creating file: {file_name}")
    try:
        folder_path.mkdir(parents=True, exist_ok=True)

        existed = full_path.exists()
        if existed and not overwrite:
            return {"status": False, 
                    "data": {
                        "file_path": str(full_path),
                        "created": False,
                        "error": "file_exists"
                    },
                    "message": f"File {file_name} already exists"
                }

        with open(full_path, "w") as f:
            f.write("")
        return {
            "status": True,
            "data": {
                "file_path": str(full_path),
                "created": True,
            },
            "message": f"File {file_name} created successfully"
        }
    except Exception as e:
        error_logger.log_error(f"file_management.create_file: Error creating file: {file_name}: {e}")
        return {
            "status": False,
            "data": {
                "file_path": str(full_path),
                "created": False,
                "error": str(e)
            },
            "message": f"Error creating file: {file_name}: {e}"
        }

@version("1.0.0")
def delete_file(file_path: str, file_name: str) -> dict:
    """
    Delete a file
    """

    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name

    technical_logger.log_info(f"file_management.delete_file: Deleting file: {file_name}")
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
        return {
            "status": True,
            "data": {
                "file_path": str(full_path),
                "deleted": True,
            },
            "message": f"File {file_name} deleted successfully"
        }
    except Exception as e:
        error_logger.log_error(f"file_management.delete_file: Error deleting file: {file_name}: {e}")
        return {
            "status": False,
            "data": {
                "file_path": str(full_path),
                "deleted": False,
                "error": str(e)
            },
            "message": f"Error deleting file: {file_name}: {e}"
        }

@version("1.0.0")
def read_file(file_path: str, file_name: str) -> dict:
    """
    Read a file
    """
    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name

    technical_logger.log_info(f"file_management.read_file: Reading file: {file_name}")
    try:
        with open(full_path, "r") as f:
            return {
                "status": True,
                "data": {
                    "file_path": full_path,
                    "file_name": file_name,
                    "file_content": f.read(),
                    "file_size": os.path.getsize(full_path)
                },
                "message": f"File {file_name} read successfully"
            }
    except Exception as e:
        error_logger.log_error(f"file_management.read_file: Error reading file: {file_name}: {e}")
        return {
            "status": False,
            "data": {
                "file_path": str(full_path),
                "file_name": file_name,
                "file_content": None,
                "file_size": os.path.getsize(full_path),
                "error": str(e)
            },
            "message": f"Error reading file: {file_name}: {e}"
        }
    
@version("1.0.0")
def write_file(file_path: str, file_name: str, content: str) -> dict:
    """
    Write to a file
    """
    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name

    try:
        technical_logger.log_info(f"file_management.write_file: Writing to file: {file_name}")
        with open(full_path, "w") as f:
            f.write(content)
        return {
            "status": True,
            "data": {
                "file_path": str(full_path),
                "file_name": file_name,
                "file_content": content,
                "file_size": os.path.getsize(full_path)
            },
            "message": f"File {file_name} written successfully"
        }
    except Exception as e:
        error_logger.log_error(f"file_management.write_file: Error writing to file: {file_name}: {e}")
        return {
            "status": False,
            "data": {
                "file_path": str(full_path),
                "file_name": file_name,
                "file_content": content,
                "file_size": os.path.getsize(full_path),
                "error": str(e)
            },
            "message": f"Error writing to file: {file_name}: {e}"
        }

@version("1.0.0")
def append_file(file_path: str, file_name: str, content: str) -> dict:
    """
    Append to a file
    """
    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name

    technical_logger.log_info(f"file_management.append_file: Appending to file: {file_name}")
    try:
        with open(full_path, "a") as f:
            f.write(content)
        return {
            "status": True,
            "data": {
                "file_path": str(full_path),
                "file_name": file_name,
                "file_content": content,
                "file_size": os.path.getsize(full_path)
            },
            "message": f"File {file_name} appended successfully"
        }
    except Exception as e:
        error_logger.log_error(f"file_management.write_file: Error writing to file: {file_name}: {e}")
        return {
            "status": False,
            "data": {
                "file_path": str(full_path),
                "file_name": file_name,
                "error": str(e)
            },
            "message": f"Error writing to file: {file_name}: {e}"
        }

@version("1.0.0")
def list_files(directory_path: str) -> dict:
    """
    List all files in a directory
    """
    folder_path = PROJECT_ROOT / directory_path

    technical_logger.log_info(f"file_management.list_files: Listing files in directory: {directory_path}")
    try:
        return {
            "status": True,
            "data": {
                "directory_path": folder_path,
                "files": os.listdir(folder_path)
            },
            "message": f"Files in directory {directory_path} listed successfully"
        }
    except Exception as e:
        error_logger.log_error(f"file_management.list_files: Error listing files in directory: {directory_path}: {e}")
        return {
            "status": False,
            "data": {
                "directory_path": str(folder_path),
                "error": str(e)
            },
            "message": f"Error listing files in directory: {directory_path}: {e}"
        }

@version("1.0.0")
def list_directories(directory_path: str) -> dict:
    """
    List all directories in a directory
    """
    folder_path = PROJECT_ROOT / directory_path

    technical_logger.log_info(f"file_management.list_directories: Listing directories in directory: {directory_path}")
    try:
        return {
            "status": True,
            "data": {
                "directory_path": folder_path,
                "directories": [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
            },
            "message": f"Directories in directory {directory_path} listed successfully"
        }
    except Exception as e:
        error_logger.log_error(f"file_management.list_directories: Error listing directories in directory: {directory_path}: {e}")
        return {
            "success": False,
            "data": {
                "directory_path": str(folder_path),
                "error": str(e)
            },
            "message": f"Error listing directories in directory: {directory_path}: {e}"
        }

@version("1.0.0")
def move_file(file_path: str, file_name: str, destination_path: str) -> dict:
    """
    Move a file to a destination directory
    """

    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name
    destination_folder_path = PROJECT_ROOT / destination_path
    destination_full_path = destination_folder_path / file_name

    technical_logger.log_info(f"file_management.move_file: Moving file: {file_name} to {destination_path}")
    try:
        if os.path.exists(full_path):
            shutil.move(full_path, destination_full_path)
        return {
            "status": True,
            "data": {
                "old_file_path": full_path,
                "new_file_path": destination_full_path,
                "file_name": file_name
            },
            "message": f"File {file_name} moved successfully to {destination_path}"
        }
    except Exception as e:
        error_logger.log_error(f"file_management.move_file: Error moving file: {file_name} to {destination_path}: {e}")
        return {
            "status": False,
            "data": {
                "original_file_path": str(full_path),
                "copy_file_path": str(destination_full_path),
                "error": str(e)
            },
            "message": f"Error moving file: {file_name} to {destination_path}: {e}"
        }
    
@version("1.0.0")
def copy_file(file_path: str, file_name: str, destination_path: str) -> dict:
    """
    Copy a file to a destination directory
    """
    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name
    destination_folder_path = PROJECT_ROOT / destination_path
    destination_full_path = destination_folder_path / file_name

    technical_logger.log_info(f"file_management.copy_file: Copying file: {file_name} to {destination_path}")
    try:
        if os.path.exists(full_path):
            shutil.copy(full_path, destination_full_path)
        return {
            "status": True,
            "data": {
                "original_file_path": full_path,
                "copy_file_path": destination_full_path,
                "file_name": file_name
            },
            "message": f"File {file_name} copied successfully to {destination_path}"
        }
    except Exception as e:
        error_logger.log_error(f"file_management.copy_file: Error copying file: {file_name} to {destination_path}: {e}")
        return {
            "status": False,
            "data": {
                "original_file_path": str(full_path),
                "copy_file_path": str(destination_full_path),
                "error": str(e)
            },
            "message": f"Error copying file: {file_name} to {destination_path}: {e}"
        }

@version("1.0.0")
def rename_file(file_path: str, file_name: str, new_name: str) -> dict:
    """
    Rename a file
    """
    folder_path = PROJECT_ROOT / file_path
    old_path = folder_path / file_name
    new_path = folder_path / new_name

    technical_logger.log_info(f"file_management.rename_file: Renaming file: {file_name} to {new_name}")
    try:
        if os.path.exists(old_path) and not os.path.exists(new_path):
            os.rename(old_path, new_path)
        return {
            "status": True,
            "data": {
                "old_file_name": file_name,
                "new_file_name": new_name,
                "file_name": new_name
            },
            "message": f"File {file_name} renamed successfully to {new_name}"
        }
    except Exception as e:
        error_logger.log_error(f"file_management.rename_file: Error renaming file: {file_name} to {new_name}: {e}")
        return {
            "status": False,
            "data": {
                "old_file_name": file_name,
                "new_file_name": new_name,
                "error": str(e)
            },
            "message": f"Error renaming file: {file_name} to {new_name}: {e}"
        }

@version("1.0.0")
def file_exists(file_path: str, file_name: str) -> dict:
    """
    Check if a file exists
    """
    folder_path = PROJECT_ROOT / file_path
    full_path = folder_path / file_name

    technical_logger.log_info(f"file_management.file_exists: Checking if file exists: {file_name} in {file_path}")
    try:
        if os.path.exists(full_path):
            return {
                "status": True,
                "data": {
                    "file_path": full_path,
                    "file_name": file_name,
                    "file_exists": True
                },
                "message": f"File {file_name} exists in {file_path}"
            }
        else:
            return {
                "status": False,
                "data": {
                    "file_path": full_path,
                    "file_name": file_name,
                    "file_exists": False
                },
                "message": f"File {file_name} does not exist in {file_path}"
            }
        
    except Exception as e:
        error_logger.log_error(f"file_management.file_exists: Error checking if file exists: {file_name} in {file_path}: {e}")
        return {
            "status": False,
            "data": {
                "file_path": str(full_path),
                "file_name": file_name,
                "error": str(e)
            },
            "message": f"Error checking if file exists: {file_name} in {file_path}: {e}"
        }

@version("1.0.0")
def directory_exists(directory_path: str) -> dict:
    """
    Check if a directory exists
    """
    folder_path = PROJECT_ROOT / directory_path

    technical_logger.log_info(f"file_management.directory_exists: Checking if directory exists: {directory_path}")
    try:
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            return {
                "status": True,
                "data": {
                    "directory_path": folder_path,
                    "directory_exists": True
                },
                "message": f"Directory {directory_path} exists"
            }
        else:
            return {
                "status": False,
                "data": {
                    "directory_path": folder_path,
                    "directory_exists": False
                },
                "message": f"Directory {directory_path} does not exist"
            }
    except Exception as e:
        error_logger.log_error(f"file_management.directory_exists: Error checking if directory exists: {directory_path}: {e}")
        return {
            "status": False,
            "data": {
                "directory_path": str(folder_path),
                "error": str(e)
            },
            "message": f"Error checking if directory exists: {directory_path}: {e}"
        }

    
        
