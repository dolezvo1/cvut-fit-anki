#!/usr/bin/env python3

import sys
import csv
import random
from xml.dom import minidom
from pathlib import Path

def sanitize_field_text(s):
    if s is None:
        return ""
    # Prevent closing the field element accidentally
    return s.replace("</field>", "<!/field>")

def row_to_note_xml(fields, note_id="", note_type=""):
    parts = [f'    <note id="{note_id}" type="{note_type}">']
    for f in fields:
        parts.append('        <div class="field">')
        parts.append(sanitize_field_text(f))
        parts.append('        </div>')
    parts.append('    </note>')
    return "\n".join(parts)

def tsv_to_xml(input_tsv, output_xml):
    lines = []
    lines.append('<?xml version="1.0" encoding="utf-8"?>')
    lines.append('<deck>')

    with open(input_tsv, newline='', encoding='utf-8') as fh:
        reader = csv.reader(fh, delimiter="\t")
        rows = []
        for row in reader:
            if not any(cell.strip() for cell in row):
                continue
            rows.append([row[2] if len(row) > 2 else "", [cell for idx, cell in enumerate(row) if idx <= 1]])
            
        rows.sort()
        for _, fields in rows:
            note_xml = row_to_note_xml(fields, str(random.randrange(1 << 30, 1 << 31)), str(1708237251))
            lines.append(note_xml)
    lines.append('</deck>')

    content = "\n".join(lines) + "\n"
    Path(output_xml).write_text(content, encoding='utf-8')
    print(f"Wrote: {output_xml}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 tsv_to_xml.py input.tsv output.xml", file=sys.stderr)
        sys.exit(2)
    input_tsv = sys.argv[1]
    output_xml = sys.argv[2]
    tsv_to_xml(input_tsv, output_xml)

if __name__ == "__main__":
    main()
