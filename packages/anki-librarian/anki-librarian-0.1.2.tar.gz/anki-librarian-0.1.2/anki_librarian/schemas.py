from pathlib import Path
from typing import Any, Dict, List

import genanki
from pydantic import BaseModel, Field

RawNote = List[str]


class Note(BaseModel):
    model_name: str
    fields: List[str]

    def to_card_model(self, models):
        return genanki.Note(model=models[self.model_name], fields=self.fields)


class NoteSpec(BaseModel):
    model_name: str = Field(alias="model")
    notes: List[RawNote]

    def generate_notes(self):
        for note in self.notes:
            yield Note(model_name=self.model_name, fields=note)


class CardDoc(BaseModel):
    cards: NoteSpec = None

    def notes(self):
        if self.cards:
            return list(self.cards.generate_notes())
        return []


class Model(BaseModel):
    id: int
    name: str
    fields: List[Dict]
    templates: List[Dict]

    def to_card_model(self):
        return genanki.Model(
            model_id=self.id,
            name=self.name,
            fields=self.fields,
            templates=self.templates,
        )


class Deck(BaseModel):
    id: int
    directory: Path
    name: str
    models: List[Model]
    notes: List[Note] = []

    def to_card_model(self):
        deck = genanki.Deck(
            deck_id=self.id,
            name=self.name,
        )

        models = {m.name: m.to_card_model() for m in self.models}

        for note in self.notes:
            deck.add_note(note.to_card_model(models))

        return deck

    def load_notes(self, path):
        for model_name, note_fields in all_deck_notes(deck_path, deck):
            deck.add_note(Note(model=models[model_name], fields=note_fields))

    def write_to_directory(self, directory):
        deck = self.to_card_model()
        genanki.Package(deck).write_to_file(directory / f"{self.directory.name}.apkg")
