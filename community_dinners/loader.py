import json
from pathlib import Path
def load_dict(path):
    """Load JSON file and return dictionary."""
    with open(path, 'r') as f:
        dict_data = json.load(f)
    return dict_data
 
def load_json_key(path, key):
    """Load specific key from JSON file."""
    dict_data = load_dict(path)
    return dict_data[key]
 
def save_dict(path, data):
    """Save dictionary to JSON file."""
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def save_json_key(path, key, data):
    """Save specific key to JSON file."""
    # Load existing data
    try:
        existing_data = load_dict(path)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}
    
    # Update with new data
    existing_data[key] = data
    
    # Save back to file
    save_dict(path, existing_data)

def load_dataset(base_dir):
    """Load families and persons data from base directory."""
    base_dir = Path(base_dir)
    
    # Load raw JSON data
    families_list_dict = load_json_key(base_dir / "families.json", "families")
    persons_list_dict = load_json_key(base_dir / "persons.json", "persons")
    
    return families_list_dict, persons_list_dict
