"""
Tools for interacting with Obsidian.
"""

from datetime import datetime
from utilities.logger import Logger
import json

from ai_tools import file_management as fm
from ai_tools import format as fmt
from utilities.decorators import version


error_logger = Logger("error")
technical_logger = Logger("technical")

@version("1.0.0")
def set_active_vault(vault_name: str) -> dict:
    """
    Set the active vault.
    """
    technical_logger.log_info(f"obsidian.set_active_vault: Setting active vault {vault_name}")
    try:
        # Check if the vault exists
        if not fm.directory_exists(f"vaults/{vault_name}"):
            error_logger.log_error(f"obsidian.set_active_vault: Vault {vault_name} does not exist")
            return False
         
        # Now set the target vault as active
        vault_metadata_path = f"vaults/{vault_name}"
        vault_metadata_content = fm.read_file(vault_metadata_path, "vault_metadata.json")
        vault_metadata = json.loads(vault_metadata_content)
        
        # Set the active vault
        vault_metadata["vault_active"] = True
        
        # Write the vault metadata file
        fm.write_file(vault_metadata_path, "vault_metadata.json", json.dumps(vault_metadata, indent=4))

        # Log the success
        technical_logger.log_info(f"obsidian.set_active_vault: Vault {vault_name} set as active")
        return {"status": True, 
                "data": {
                    "vault_name": vault_name,
                    "vault_path": str(vault_metadata_path)
                },
                "message": f"Vault {vault_name} set as active"
            }
    
    # If an error occurs, log the error and return False
    except Exception as e:
        error_logger.log_error(f"obsidian.set_active_vault: Error setting active vault {vault_name}: {e}")
        return {"status": False, 
                "data": {
                    "vault_name": vault_name,
                    "error": str(e)
                },
                "message": f"Error setting active vault {vault_name}: {e}"
            }

@version("1.0.0")
def deactivate_vault(vault_name: str) -> dict:
    """
    Set the inactive vault.
    """
    technical_logger.log_info(f"obsidian.deactivate_vault: Deactivating vault {vault_name}")
    try:
        # Check if the vault exists
        if not fm.directory_exists(f"vaults/{vault_name}"):
            error_logger.log_error(f"obsidian.deactivate_vault: Vault {vault_name} does not exist")
            return {"status": False, 
                    "data": {
                        "vault_name": vault_name,
                        "error": "vault_not_found"
                    },
                    "message": f"Vault {vault_name} does not exist"
                }
        
        # Read the vault metadata file
        vault_metadata = fm.read_file(f"vaults/{vault_name}", "vault_metadata.json")
        vault_metadata = json.loads(vault_metadata)
        
        # Set the inactive vault
        vault_metadata["vault_active"] = False
        
        # Write the vault metadata file
        fm.write_file(f"vaults/{vault_name}", "vault_metadata.json", json.dumps(vault_metadata, indent=4))
        
        # Log the success
        technical_logger.log_info(f"obsidian.deactivate_vault: Vault {vault_name} set as inactive")
        return {"status": True, 
                "data": {
                    "vault_name": vault_name,
                    "vault_active": False
                },
                "message": f"Vault {vault_name} set as inactive"
            }
    
    # If an error occurs, log the error and return False
    except Exception as e:
        error_logger.log_error(f"obsidian.deactivate_vault: Error setting inactive vault {vault_name}: {e}")
        return {"status": False, 
                "data": {
                    "vault_name": vault_name,
                    "error": str(e)
                },
                "message": f"Error setting inactive vault {vault_name}: {e}"
            }
    
@version("1.0.0")
def get_active_vault() -> dict:
    """
    Find the active vault by searching through each vault folder for vault_metadata.json.
    """
    try:
        technical_logger.log_info("obsidian.get_active_vault: Finding active vault")

        # Check if vaults directory exists
        if not fm.directory_exists("vaults"):
            error_logger.log_error("obsidian.get_active_vault: Vaults directory does not exist")
            return {"status": False, 
                    "data": {
                        "error": "vaults_directory_not_found"
                    },
                    "message": "Vaults directory does not exist"
                }
        
        # Get all vault directories
        vault_directories = fm.list_directories("vaults")
        
        # Search through each vault directory for vault_metadata.json
        for vault_name in vault_directories:
            vault_metadata_path = f"vaults/{vault_name}"
            
            # Check if vault_metadata.json exists
            if fm.file_exists(vault_metadata_path, "vault_metadata.json"):
                # Read the vault metadata file
                vault_metadata_content = fm.read_file(vault_metadata_path, "vault_metadata.json")
                if vault_metadata_content:
                    vault_metadata = json.loads(vault_metadata_content)
                    
                    # Check if this vault is active
                    if vault_metadata.get("vault_active", False):
                        technical_logger.log_info(f"obsidian.get_active_vault: Found active vault: {vault_name}")
                        return {"status": True, 
                                "data": {
                                    "active_vault": vault_name
                                },
                                "message": f"Found active vault: {vault_name}"
                            }
        
        # If no active vault is found, return None
        error_logger.log_error("obsidian.get_active_vault: No active vault found")
        return {"status": True, 
                "data": {
                    "active_vault": None
                },
                "message": "No active vault found"
            }
    
    # If an error occurs, log the error and return None
    except Exception as e:
        error_logger.log_error(f"obsidian.get_active_vault: Error getting active vault: {e}")
        return {"status": False, 
                "data": {
                    "error": str(e)
                },
                "message": f"Error getting active vault: {e}"
            }
    
# Command
@version("1.0.0")
def deactivate_all_vaults() -> dict:
    """
    Deactivate all vaults.
    """
    technical_logger.log_info("obsidian.deactivate_all_vaults: Deactivating all vaults")
    try:
        # Get all vault directories
        vault_directories = fm.list_directories("vaults")
        
        # Deactivate all vaults
        for other_vault in vault_directories:
            other_vault_metadata_path = f"vaults/{other_vault}"
            if fm.file_exists(other_vault_metadata_path, "vault_metadata.json"):
                try:
                    other_vault_metadata_content = fm.read_file(other_vault_metadata_path, "vault_metadata.json")
                    if other_vault_metadata_content:
                        other_vault_metadata = json.loads(other_vault_metadata_content)
                        other_vault_metadata["vault_active"] = False
                        fm.write_file(other_vault_metadata_path, "vault_metadata.json", json.dumps(other_vault_metadata, indent=4))
                        technical_logger.log_info(f"obsidian.deactivate_all_vaults: Deactivated vault: {other_vault}")
                except Exception as e:
                    error_logger.log_error(f"obsidian.deactivate_all_vaults: Error deactivating vault {other_vault}: {e}")
        
        # Log the success
        technical_logger.log_info("obsidian.deactivate_all_vaults: All vaults deactivated")
        return {"status": True, 
                "data": {
                    "deactivated_vaults": vault_directories
                },
                "message": "All vaults deactivated"
            }
    # If an error occurs, log the error and return False
    except Exception as e:
        error_logger.log_error(f"obsidian.deactivate_all_vaults: Error deactivating all vaults: {e}")
        return {"status": False, 
                "data": {
                    "error": str(e)
                },
                "message": f"Error deactivating all vaults: {e}"
            }

# Command    
@version("1.0.0")
def swap_active_vault(vault_name: str) -> dict:
    """
    Swap the active vault.
    """
    technical_logger.log_info("obsidian.swap_active_vault: Swapping active vault")
    try:
        # Get the active vault
        active_vault = get_active_vault()
        
        # Deactivate all vaults
        deactivate_all_vaults()
        
        # Set the new active vault
        set_active_vault(vault_name)
        
        # Log the success
        if active_vault:
            technical_logger.log_info(f"Swapped active vault from {active_vault} to {vault_name}")
        else:
            technical_logger.log_info(f"Set active vault to {vault_name}")
        return {"status": True, 
                "data": {
                    "active_vault": vault_name,
                    "deactivated_vault": active_vault
                },
                "message": f"Swapped active vault from {active_vault} to {vault_name}"
            }

    # If an error occurs, log the error and return False
    except Exception as e:
        error_logger.log_error(f"obsidian.swap_active_vault: Error swapping active vault: {e}")
        return {"status": False, 
                "data": {
                    "error": str(e)
                },
                "message": f"Error swapping active vault: {e}"
            }
    
@version("1.0.0")
def list_vaults() -> dict:
    """
    List all vaults.
    """
    try:
        # Get all vault directories
        vault_directories = fm.list_directories("vaults")

        # Return the vault directories
        return {"status": True, 
                "data": {
                    "vault_directories": vault_directories
                },
                "message": "Vaults listed"
            }
    
    # If an error occurs, log the error and return None
    except Exception as e:
        error_logger.log_error(f"obsidian.list_vaults: Error listing vaults: {e}")
        return {"status": False, 
                "data": {
                    "error": str(e)
                },
                "message": f"Error listing vaults: {e}"
            }
    
# Command
@version("1.0.0")
def confirm_vault_setup(vault_name: str) -> dict:
    """
    Confirm the vault has all the necessary directories and files.

    Directories:
    - vaults/{vault_name}
    - vaults/{vault_name}/{vault_name}
    - raw/{vault_name}
    - processed/{vault_name}
    - vaults/{vault_name}/note_templates

    Files:
    - vaults/{vault_name}/vault_metadata.json
    - vaults/{vault_name}/books.json
    - vaults/{vault_name}/vault_map.json
    """
    try:
        # Check if the vault exists
        if not fm.directory_exists(f"vaults/{vault_name}"):
            error_logger.log_error(f"obsidian.confirm_vault_setup: Vault {vault_name} does not exist")
            return {"status": False, 
                    "data": {
                        "vault_name": vault_name,
                        "error": "vault_root_directory_not_found"
                    },
                    "message": f"Vault root directory {vault_name} does not exist"
                }
        
        # Check if the vault has all the necessary directories
        if not fm.directory_exists(f"vaults/{vault_name}/{vault_name}"):
            error_logger.log_error(f"obsidian.confirm_vault_setup: Vault {vault_name} does not have a {vault_name} directory")
            return {"status": False, 
                    "data": {
                        "vault_name": vault_name,
                        "error": "vault_notes_directory_not_found"
                    },
                    "message": f"Vault {vault_name} does not have a {vault_name} notes directory"
                }
        
        if not fm.directory_exists(f"raw/{vault_name}"):
            error_logger.log_error(f"obsidian.confirm_vault_setup: Vault {vault_name} does not have a raw directory")
            return {"status": False, 
                    "data": {
                        "vault_name": vault_name,
                        "error": "vault_raw_directory_not_found"
                    },
                    "message": f"Vault {vault_name} does not have a raw directory"
                }
        
        if not fm.directory_exists(f"processed/{vault_name}"):
            error_logger.log_error(f"obsidian.confirm_vault_setup: Vault {vault_name} does not have a processed directory")
            return {"status": False, 
                    "data": {
                        "vault_name": vault_name,
                        "error": "vault_processed_directory_not_found"
                    },
                    "message": f"Vault {vault_name} does not have a processed directory"
                }
        
        if not fm.directory_exists(f"vaults/{vault_name}/note_templates"):
            error_logger.log_error(f"obsidian.confirm_vault_setup: Vault {vault_name} does not have a note_templates directory")
            return {"status": False, 
                    "data": {
                        "vault_name": vault_name,
                        "error": "vault_note_templates_directory_not_found"
                    },
                    "message": f"Vault {vault_name} does not have a note_templates directory"
                }
        
        # Check if the vault has all the necessary files
        if not fm.file_exists(f"vaults/{vault_name}/vault_metadata.json"):
            error_logger.log_error(f"obsidian.confirm_vault_setup: Vault {vault_name} does not have a vault_metadata.json file")
            return {"status": False, 
                    "data": {
                        "vault_name": vault_name,
                        "error": "vault_metadata_file_not_found"
                    },
                    "message": f"Vault {vault_name} does not have a vault_metadata.json file"
                }
        
        if not fm.file_exists(f"vaults/{vault_name}/books.json"):
            error_logger.log_error(f"obsidian.confirm_vault_setup: Vault {vault_name} does not have a books.json file")
            return {"status": False, 
                    "data": {
                        "vault_name": vault_name,
                        "error": "vault_books_file_not_found"
                    },
                    "message": f"Vault {vault_name} does not have a books.json file"
                }
        
        if not fm.file_exists(f"vaults/{vault_name}/vault_map.json"):
            error_logger.log_error(f"obsidian.confirm_vault_setup: Vault {vault_name} does not have a vault_map.json file")
            return {"status": False, 
                    "data": {
                        "vault_name": vault_name,
                        "error": "vault_map_file_not_found"
                    },
                    "message": f"Vault {vault_name} does not have a vault_map.json file"
                }
        
        # Log the success
        technical_logger.log_info(f"obsidian.confirm_vault_setup: Vault {vault_name} has all the necessary directories and files")
        return {"status": True, 
                "data": {
                    "vault_name": vault_name
                },
                "message": f"Vault {vault_name} has all the necessary directories and files"
            }
    
    # If an error occurs, log the error and return False
    except Exception as e:
        error_logger.log_error(f"obsidian.confirm_vault_setup: Error confirming vault setup: {e}")
        return {"status": False, 
                "data": {
                    "vault_name": vault_name,
                    "error": str(e)
                },
                "message": f"Error confirming vault setup: {e}"
            }
    
@version("1.0.0")
def create_note(note_name: str, note_content: str, note_path: str) -> dict:
    """
    Create a new note.
    """
    try:
        # Check if the note already exists
        if fm.file_exists(note_path):
            error_logger.log_error(f"Note {note_name} already exists in {note_path}")
            return {"status": False, 
                    "data": {
                        "note_name": note_name,
                        "note_path": note_path,
                        "error": "note_already_exists"
                    },
                    "message": f"Note {note_name} already exists in {note_path}"
                }

        # Get the active vault
        active_vault = get_active_vault()

        # Create the note
        fm.create_file(note_path, note_name)

        # Write the note content to the file
        fm.write_file(note_path, note_name, note_content)

        # Log the success
        technical_logger.log_info(f"Note {note_name} created successfully in {note_path}")
        return {"status": True, 
                "data": {
                    "note_name": note_name,
                    "note_path": note_path
                },
                "message": f"Note {note_name} created successfully in {note_path}"
            }

    # If an error occurs, log the error and return False
    except Exception as e:
        error_logger.log_error(f"Error creating note {note_name} in {note_path}: {e}")
        return {"status": False, 
                "data": {
                    "note_name": note_name,
                    "note_path": note_path,
                    "error": str(e)
                },
                "message": f"Error creating note {note_name} in {note_path}: {e}"
            }
    
@version("1.0.0")
def get_tags() -> dict:
    """
    Get the tags for the active vault.
    """
    try:
        # Get the active vault
        active_vault = get_active_vault()
    
        # Get the tags from the vault metadata
        vault_metadata = fm.read_file(f"vaults/{active_vault}", "vault_metadata.json")
        vault_metadata = json.loads(vault_metadata)
        tags = vault_metadata.get("tags", {})
        
        # Return the tags
        return {"status": True, 
                "data": {
                    "tags": list(tags.keys())
                },
                "message": "Tags listed"
            }
    
    # If an error occurs, log the error and return None
    except Exception as e:
        error_logger.log_error(f"Error getting tags: {e}")
        return {"status": False, 
                "data": {
                    "error": str(e)
                },
                "message": f"Error getting tags: {e}"
            }
    
@version("1.0.0")
def add_tag(tag: str) -> dict:
    """
    Add a tag to the active vault.
    """
    try:
        # Get the active vault
        active_vault = get_active_vault()
        
        # Get the tags from the vault metadata
        vault_metadata = fm.read_file(f"vaults/{active_vault}", "vault_metadata.json")
        vault_metadata = json.loads(vault_metadata)
        tags = vault_metadata.get("tags", {})
        
        # Add the tag to the tags dictionary
        tags[tag] = tag
        
        # Write the vault metadata file
        fm.write_file(f"vaults/{active_vault}", "vault_metadata.json", json.dumps(vault_metadata, indent=4))
        
        # Log the success
        technical_logger.log_info(f"Tag {tag} added to {active_vault}")
        return {"status": True, 
                "data": {
                    "vault_name": active_vault,
                    "new_tag": tag,
                    "tags": list(tags.keys())
                },
                "message": f"Tag {tag} added to {active_vault}"
            }
    
    # If an error occurs, log the error and return False
    except Exception as e:
        error_logger.log_error(f"Error adding tag {tag} to {active_vault}: {e}")
        return {"status": False, 
                "data": {
                    "error": str(e)
                },
                "message": f"Error adding tag {tag} to {active_vault}: {e}"
            }

@version("1.0.0")
def add_tags(tags: str) -> dict:
    """
    Add tags to the active vault.
    """
    try:
        # Get the active vault
        active_vault = get_active_vault()

        # Get the tags from the vault metadata
        vault_metadata = fm.read_file(f"vaults/{active_vault}", "vault_metadata.json")
        vault_metadata = json.loads(vault_metadata)
        vault_tags = vault_metadata.get("tags", {})

        # Load the tags from the JSON string
        tags_json = json.loads(tags)
        new_tags = tags_json.get("tags", [])

        # Add the tags to the tags dictionary
        for tag in new_tags:
            if tag not in vault_tags:
                vault_tags[tag] = tag

        # Write the vault metadata file
        fm.write_file(f"vaults/{active_vault}", "vault_metadata.json", json.dumps(vault_metadata, indent=4))

        # Log the success
        technical_logger.log_info(f"Tags {tags} added to {active_vault}")
        return {"status": True, 
                "data": {
                    "vault_name": active_vault,
                    "new_tags": tags,
                    "tags": list(vault_tags.keys())
                },
                "message": f"Tags {tags} added to {active_vault}"
            }
    
    # If an error occurs, log the error and return False
    except Exception as e:
        error_logger.log_error(f"Error adding tags {tags} to {active_vault}: {e}")
        return {"status": False, 
                "data": {
                    "error": str(e)
                },
                "message": f"Error adding tags {tags} to {active_vault}: {e}"
            }

@version("1.0.0")
def remove_tag(tag: str) -> dict:
    """
    Remove a tag from the active vault.
    """
    try:
        # Get the active vault
        active_vault = get_active_vault()
        
        # Get the tags from the vault metadata
        vault_metadata = fm.read_file(f"vaults/{active_vault}", "vault_metadata.json")
        vault_metadata = json.loads(vault_metadata)
        tags = vault_metadata.get("tags", {})
        
        # Remove the tag from the tags dictionary
        del tags[tag]
        
        # Write the vault metadata file
        fm.write_file(f"vaults/{active_vault}", "vault_metadata.json", json.dumps(vault_metadata, indent=4))

        # Log the success
        technical_logger.log_info(f"Tag {tag} removed from {active_vault}")
        return {"status": True, 
                "data": {
                    "vault_name": active_vault,
                    "removed_tag": tag,
                    "tags": list(tags.keys())
                },
                "message": f"Tag {tag} removed from {active_vault}"
            }
    
    # If an error occurs, log the error and return False
    except Exception as e:
        error_logger.log_error(f"Error removing tag {tag} from {active_vault}: {e}")
        return {"status": False, 
                "data": {
                    "error": str(e)
                },
                "message": f"Error removing tag {tag} from {active_vault}: {e}"
            }
    
@version("1.0.0")
def create_note_metadata(note_title: str, note_type: str, tags: list) -> dict:
    """
    Create a note metadata file.
    """
    technical_logger.log_info(f"obsidian.create_note_metadata: Creating note metadata for {note_title}")

    try:
        # Get the active vault
        #active_vault = get_active_vault()
        
        # Create the note metadata file
        metadata = f"""---\nTitle: {note_title}\nDate Created: {datetime.now().isoformat()}\nLast Updated: {datetime.now().isoformat()}\nType: {note_type}\ntags:\n""" + fmt.format_tags(tags) + "\n---"
        
        technical_logger.log_info(f"obsidian.create_note_metadata: Delivered note metadata for {note_title}")
        return {"status": True, 
                "data": {
                    "note_title": note_title,
                    "note_type": note_type,
                    "tags": tags
                },
                "message": f"Note metadata created for {note_title}"
            }
    
    # If an error occurs, log the error and return None
    except Exception as e:
        error_logger.log_error(f"obsidian.create_note_metadata: Error creating note metadata: {e}")
        return {"status": False, 
                "data": {
                    "error": str(e)
                },
                "message": f"Error creating note metadata: {e}"
            }
        
#def get_vault_local_model() -> str:
#    """
#    Get the local model for the active vault.
#    """
#    try:
#        # Get the active vault
#        active_vault = get_active_vault()
        
        # Get the local model from the vault metadata
        