import os
import hashlib
import json
from pathlib import Path

HASH_FILE = 'hashes.json'

def calculate_file_hash(filepath):
    """Calculate SHA-256 hash of the file."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def scan_directory(directory):
    """Scan the directory and return a dictionary of file paths and their hashes."""
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, directory)
            file_hash = calculate_file_hash(full_path)
            if file_hash:
                file_hashes[rel_path] = file_hash
    return file_hashes

def load_previous_hashes():
    """Load the previous hash values from file."""
    if Path(HASH_FILE).exists():
        with open(HASH_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    """Save current hashes to file."""
    with open(HASH_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)

def compare_hashes(old_hashes, new_hashes):
    """Compare old and new hash dictionaries."""
    changes = {
        'modified': [],
        'new': [],
        'deleted': []
    }

    old_files = set(old_hashes.keys())
    new_files = set(new_hashes.keys())

    for file in old_files & new_files:
        if old_hashes[file] != new_hashes[file]:
            changes['modified'].append(file)

    for file in new_files - old_files:
        changes['new'].append(file)

    for file in old_files - new_files:
        changes['deleted'].append(file)

    return changes

def main():
    directory = input("Enter the directory to monitor: ").strip()
    if not os.path.isdir(directory):
        print("Invalid directory path.")
        return

    print("Scanning directory...")
    new_hashes = scan_directory(directory)
    old_hashes = load_previous_hashes()
    
    changes = compare_hashes(old_hashes, new_hashes)

    print("\nChanges detected:")
    if any(changes.values()):
        for change_type, files in changes.items():
            print(f"\n{change_type.upper()} FILES:")
            for file in files:
                print(f"  - {file}")
    else:
        print("No changes detected.")

    save_hashes(new_hashes)
    print("\nHashes updated.")

if __name__ == "__main__":
    main()