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

class ExportManager:
    def __init__(self):
        self.source_decks = []
        self.source_resources = []
    
    def add_all_decks_in(self, path):
        for dirpath, dirnames, filenames in os.walk(path):
            if '_deck.xml' in filenames:
                self.source_decks.append(os.path.join(dirpath, '_deck.xml'))
                self.source_resources.extend(os.path.join(dirpath, n) for n in filenames if n != '_deck.xml')
    
    def get_unique_requested_paths(self):
        return list(set(self.source_decks)), list(set(self.source_resources))

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
    parser.add_argument('--ni-spol', dest='generate_ni_spol', action='store_true')
    parser.add_argument('--ni-pb', dest='generate_ni_pb', action='store_true')
    parser.add_argument('--ni-si', dest='generate_ni_si', action='store_true')
    parser.add_argument('--ni-wi', dest='generate_ni_wi', action='store_true')
    # parser.add_argument('--add-deck', dest='specific_decks', action='append')
    args = parser.parse_args()
    # print(args)
    
    # Collect decks info as requested
    manager = ExportManager()
    if args.generate_all:
        manager.add_all_decks_in("src/")
    if args.generate_ni_spol:
        manager.add_all_decks_in("src/NI-MPI/")
        manager.add_all_decks_in("src/NI-VSM/")
        manager.add_all_decks_in("src/NI-KOP/")
        manager.add_all_decks_in("src/NI-PDP/")
    if args.generate_ni_pb:
        manager.add_all_decks_in("src/NI-HWB/")
        manager.add_all_decks_in("src/NI-KRY/")
        manager.add_all_decks_in("src/NI-MKY/")
        manager.add_all_decks_in("src/NI-AIB/")
        manager.add_all_decks_in("src/NI-REV/")
        manager.add_all_decks_in("src/NI-SIB/")
        manager.add_all_decks_in("src/NI-SBF/")
    if args.generate_ni_si:
        manager.add_all_decks_in("src/NI-ADP/")
        manager.add_all_decks_in("src/NI-AM1/")
        manager.add_all_decks_in("src/NI-FME/")
        manager.add_all_decks_in("src/NI-NSS/")
        manager.add_all_decks_in("src/NI-NUR/")
        manager.add_all_decks_in("src/NI-PDB/")
        manager.add_all_decks_in("src/NI-PIS/")
    if args.generate_ni_wi:
        manager.add_all_decks_in("src/NI-DDW/")
        manager.add_all_decks_in("src/NI-AM1/")
        manager.add_all_decks_in("src/NI-VCC/")
        manager.add_all_decks_in("src/NI-PDB/")
        manager.add_all_decks_in("src/NI-SWE/")
        manager.add_all_decks_in("src/NI-VMM/")
        manager.add_all_decks_in("src/NI-AM2/")
    
    source_decks, source_resources = manager.get_unique_requested_paths()
    
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
    # print(decks)

    package = genanki.Package(decks, source_resources)
    package.write_to_file(args.output_path)


