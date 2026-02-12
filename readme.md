# CVUT-FIT-Anki

Anki cards for ČVUT FIT SZZ in a versionable format (XML to be precise).


## Usage

To generate an `.apkg` file from the source files in the `src/` directory, run:

```
pip install genanki
python generator.py --all --output out.apkg
```

Note that this will not regenerate guids, meaning that previous versions of the cards will be overwritten when the package is imported.


## Contributing

The cards are not perfect by any means and many improvements could be made. Forks and PRs are very welcome.

To convert your existing Anki decks to XML, you can export the decks individually from Anki to txt, and then use `tsv_to_xml.py` (requires some manual cleanup).


## Copyright

Provided for educational purposes only. Copyright belongs to the respective authors. The cards were sourced from various sources, most notably the official course materials, the stellar [FIT ČVUT Anki decks by Adam Škoda](https://gitlab.com/xskoda/fit-cvut-anki) and various Anki decks found on various servers.

