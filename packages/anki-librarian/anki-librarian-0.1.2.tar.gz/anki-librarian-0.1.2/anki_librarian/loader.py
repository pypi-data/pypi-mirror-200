from pathlib import Path

import pydantic
from ruamel.yaml import YAML

from .schemas import CardDoc, Deck

yaml = YAML(typ="safe")  # default, if not specfied, is 'rt' (round-trip)


def deck_from_deck_directory(deck_path):
    deck = deck_path / "deck.yaml"

    if not deck.exists() or not deck.is_file():
        return

    print(f"Loading {deck}")

    try:
        deck = Deck.parse_obj(
            {**yaml.load(open(deck, "r").read()), "directory": deck_path}
        )
    except pydantic.error_wrappers.ValidationError as exception:
        for error in exception.errors():
            loc = ".".join(str(s) for s in error["loc"])
            print(f" err @ {loc} - {error['msg']}")
        return

    for doc in deck_path.iterdir():
        cards = CardDoc.parse_obj(yaml.load(open(doc, "r").read()))
        deck.notes.extend(cards.notes())

    return deck


def decks_from_directory(source_directory: Path):
    for folder in source_directory.iterdir():
        if not folder.is_dir():
            print(f"Skipping non-folder {folder}")

        if deck := deck_from_deck_directory(folder):
            yield deck
        else:
            print(f"No deck detected at {folder}")
