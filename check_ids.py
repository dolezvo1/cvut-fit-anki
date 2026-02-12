#!/usr/bin/env python3
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from collections import defaultdict

def find_deck_files(root_dir: Path):
    return list(root_dir.rglob("_deck.xml"))

def extract_ids(xml_path: Path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        deck_id = root.get("id")
        if deck_id is not None:
            deck_id = deck_id.strip()
        note_ids = []
        for n in root.findall(".//note"):
            note_id = n.get("id")
            if note_id is not None:
                note_id = note_id.strip()
            note_ids.append(note_id)
        return deck_id, note_ids
    except Exception as e:
        print(f"ERROR parsing {xml_path}: {e}", file=sys.stderr)
        return None, []

def main(argv):
    if len(argv) < 2:
        print("Usage: check_asdf_ids.py <src-dir>", file=sys.stderr)
        return 2

    root_dir = Path(argv[1])
    if not root_dir.is_dir():
        print(f"Directory not found: {root_dir}", file=sys.stderr)
        return 2

    files = find_deck_files(root_dir)
    if not files:
        print("No _deck.xml files found.")
        return 0

    deck_id_to_files = defaultdict(list)
    note_id_to_files = defaultdict(list)
    parse_errors = False

    for f in sorted(files):
        deck_id, note_ids = extract_ids(f)
        if deck_id is None:
            print(f"WARNING: No deck id found in {f}")
        else:
            deck_id_to_files[deck_id].append(str(f))
        for note_id in note_ids:
            if note_id is None:
                print(f"WARNING: Note without an id found in {f}")
            else:
                note_id_to_files[note_id].append(str(f))

    found_errors = False

    deck_duplicates = {i:fs for i,fs in deck_id_to_files.items() if len(fs) > 1}
    if deck_duplicates:
        print("Duplicate deck id violations found:")
        for id_val, paths in deck_duplicates.items():
            print(f"ID: {id_val}")
            for p in paths:
                print(f"  - {p}")
        found_errors = True
    
    note_duplicates = {i:fs for i,fs in note_id_to_files.items() if len(fs) > 1}
    if note_duplicates:
        print("Duplicate note id violations found:")
        for id_val, paths in note_duplicates.items():
            print(f"ID: {id_val}")
            for p in paths:
                print(f"  - {p}")
        found_errors = True

    if found_errors:
        return 1

    print("All IDs are unique.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
