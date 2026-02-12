# CVUT-FIT-Anki

Anki cards for ČVUT FIT SZZ in a versionable format (XML to be precise).


## Usage

To generate an `.apkg` file from the source files in the `src/` directory, run:

```
pip install genanki
python generator.py --all --output out.apkg
```

Note that this will not regenerate guids, meaning that previous versions of the cards will be overwritten when the package is imported.


## Deck structure

Decks are stored as `_deck.xml` files. All other files in a given directory are automatically included as the note resources.

A deck node has three attributes: `id`, `name` and `deck_slug` (which is used as a prefix for the note sorting field). For example:

```
<deck id="1446238097" name="NI-PIS::NI-PIS-02" deck_slug="NI-PIS-02">
    ...notes here...
</deck>
```

A note node has two attributes: `id` and `type` (the id of the note type). For example:

```
<note id="1834387779" type="1708237251">
    ...fields here...
</note>
```

A field node is simply a `div` element which is pasted into the note field verbatim (including the outer `div` tags). Note that XML does not permit `&nbsp;`. Note XML requires non-pair tags (`br`, `img`, etc.) to have have slash before the final `>`, for example `br` looks like `<br/>`.

## Contributing

The cards are not perfect by any means and many improvements could be made. Forks and PRs are very welcome.

To convert your existing Anki decks to XML, you can export the decks individually from Anki to txt, and then use `tsv_to_xml.py` (requires some manual cleanup).


## Copyright

Provided for educational purposes only. Copyright belongs to the respective authors. The cards were sourced from various sources, most notably the official course materials, the stellar [FIT ČVUT Anki decks by Adam Škoda](https://gitlab.com/xskoda/fit-cvut-anki) and various Anki decks found on various servers.

