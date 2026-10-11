import json
import os

def save_tickets(filepath, tickets):
    """Saves the ticket list to a JSON file."""
    # Ensure directory exists if path contains a directory
    dir_name = os.path.dirname(filepath)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(tickets, f, indent=4)

def load_tickets(filepath):
    """Loads tickets from a JSON file. Returns an empty list if file doesn't exist."""
    if not os.path.exists(filepath):
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: Malformed JSON data in {filepath}. Details: {e}")