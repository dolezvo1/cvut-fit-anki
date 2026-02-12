#!/usr/bin/env python3
# Requires: pip install genanki

import argparse
import os
import sys
import xml.etree.ElementTree as ET
import genanki
import random
import html
from pathlib import Path

def generate_deck(models, top_deck_name, path):
    print(f"Processing {path}")
    tree = ET.parse(path)
    root = tree.getroot()
    
    deck_id = int(root.attrib.get("id"))
    deck_name = top_deck_name + "::" + root.attrib.get("name")
    deck_slug = root.attrib.get("deck_slug")
    deck = genanki.Deck(deck_id, deck_name)
    
    for idx, note_elem in enumerate(root.findall(".//note")):
        fields = [ET.tostring(fld, encoding="unicode") for fld in note_elem.findall("div")]
        
        if len(fields) < 2:
            continue
        fields.append(f"{deck_slug}_{(idx + 1) * 10:04d}")
        
        note = genanki.Note(model=models[note_elem.attrib.get("type")], guid=note_elem.attrib.get("id"), fields=fields)
        deck.add_note(note)
    
    return deck


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', dest='top_deck_name', default="CVUT-FIT-Anki")
    parser.add_argument('--generate-new-uuids', action='store_true')
    parser.add_argument('--output', dest='output_path', required=True)
    parser.add_argument('--all', dest='generate_all', action='store_true')
    # parser.add_argument('--add-deck', dest='specific_decks', action='append')
    args = parser.parse_args()
    print(args)
    
    # If generate_all flag is present, scan the src location
    source_decks = []
    source_resources = []
    if args.generate_all:
        for dirpath, dirnames, filenames in os.walk('src/'):
            if '_deck.xml' in filenames:
                source_decks.append(os.path.join(dirpath, '_deck.xml'))
                source_resources.extend(os.path.join(dirpath, n) for n in filenames if n != '_deck.xml')
    else:
        # TODO: option to select specific decks
        print("'--all' must be selected at the moment")
        sys.exit(1)
    
    # Set up "models" (Note types)
    models = {}
    models["1708237251"] = genanki.Model(
        1708237251,
        "Basic+++",
        fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Sort"}],
        sort_field_index=2,
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Front}}",
                "afmt": "{{FrontSide}}<hr id=\"answer\">{{Back}}",
            },
        ],
    )
    
    # Generate decks based on sources
    decks = [generate_deck(models, args.top_deck_name, d) for d in source_decks]
    print(decks)

    package = genanki.Package(decks, source_resources)
    package.write_to_file(args.output_path)


