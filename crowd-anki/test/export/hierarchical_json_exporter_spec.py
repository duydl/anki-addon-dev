import json
import sys
from functools import cached_property
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from test_utils.anki import MockAnkiModules


class _FunctionalSeq:
    def __init__(self, iterable):
        self._iterable = list(iterable)

    def map(self, func):
        return _FunctionalSeq([func(item) for item in self._iterable])

    def make_string(self, separator):
        return separator.join(self._iterable)


def _functional_seq(iterable):
    return _FunctionalSeq(iterable)


sys.modules["cached_property"] = SimpleNamespace(cached_property=cached_property)
sys.modules["functional"] = SimpleNamespace(seq=_functional_seq)

mocked_modules = MockAnkiModules(
    MockAnkiModules.module_names_list
    + [
        "PyQt6",
        "PyQt6.QtCore",
        "PyQt6.QtGui",
        "PyQt6.QtWidgets",
        "yaml",
    ]
)
sys.modules["aqt.qt"].qtmajor = 6

from crowd_anki.export.hierarchical_json_exporter import HierarchicalJsonExporter
from crowd_anki.importer.anki_importer import AnkiJsonImporter
from crowd_anki.representation.json_serializable import JsonSerializable
from crowd_anki.utils.filesystem.name_sanitizer import sanitize_anki_deck_name


@pytest.fixture(scope="module", autouse=True)
def cleanup_mock_modules():
    yield
    mocked_modules.unmock()


class DummyNote(JsonSerializable):
    def __init__(self, guid, fields):
        super().__init__()
        self._data = {
            "__type__": "Note",
            "guid": guid,
            "fields": fields,
            "note_model_uuid": "dummy-model",
            "tags": [],
        }

    def flatten(self):
        return dict(self._data)


class DummyDeck(JsonSerializable):
    def __init__(self, name, notes=None, children=None, extra=None):
        super().__init__()
        self.anki_dict = {"name": name}
        self.notes = notes or []
        self.children = children or []
        self.extra = extra or {}
        self.metadata = MagicMock(deck_configs={}, models={})
        self.collection = MagicMock()
        self.is_child = self.extra.pop("is_child", False)

    def flatten(self):
        deck_dict = {"name": self.anki_dict["name"], "__type__": "Deck"}
        deck_dict.update(self.extra)
        deck_dict["notes"] = [note.flatten() for note in self.notes]
        deck_dict["children"] = [child.flatten() for child in self.children]
        deck_dict.setdefault("deck_configurations", [])
        deck_dict.setdefault("note_models", [])
        return deck_dict

    def get_note_count(self):
        return len(self.notes) + sum(child.get_note_count() for child in self.children)

    def get_media_file_list(self, data_from_models=True, include_children=True):
        media = set()
        if include_children:
            for child in self.children:
                media |= set(child.get_media_file_list(data_from_models, include_children))
        return media


@pytest.fixture()
def deck_setup():
    child_note = DummyNote("child-guid", ["child front", "child back"])
    child_deck = DummyDeck(
        "Child:Deck",
        notes=[child_note],
        children=[],
        extra={"deck_configurations": [{"child": "config"}]},
    )

    root_note = DummyNote("root-guid", ["root front", "root back"])
    root_deck = DummyDeck(
        "Root Deck",
        notes=[root_note],
        children=[child_deck],
        extra={
            "deck_configurations": [{"root": "config"}],
            "note_models": [{"model": "root"}],
        },
    )

    return {
        "root_deck": root_deck,
        "child_deck": child_deck,
        "root_notes": [root_note.flatten()],
        "child_notes": [child_note.flatten()],
    }


@pytest.fixture()
def exported_tree(tmp_path: Path, deck_setup):
    exporter = HierarchicalJsonExporter(MagicMock(), MagicMock())
    exporter.note_sorter = MagicMock()

    anki_deck = MagicMock()
    anki_deck.name = "Root Deck"

    with patch.object(HierarchicalJsonExporter, "_save_changes", return_value=None), patch(
        "crowd_anki.export.hierarchical_json_exporter.deck_initializer.from_collection",
        return_value=deck_setup["root_deck"],
    ):
        export_dir = exporter.export_to_directory(anki_deck, tmp_path, copy_media=False)

    return {
        "export_dir": export_dir,
        "exporter": exporter,
        **deck_setup,
    }


def test_hierarchical_exporter_creates_directory_tree(exported_tree):
    export_dir: Path = exported_tree["export_dir"]
    root_notes = exported_tree["root_notes"]
    child_notes = exported_tree["child_notes"]

    deck_json_path = export_dir / "deck.json"
    notes_json_path = export_dir / "notes.json"

    assert deck_json_path.exists()
    assert notes_json_path.exists()

    root_deck_json = json.loads(deck_json_path.read_text(encoding="utf8"))
    assert "notes" not in root_deck_json
    assert root_deck_json["children"] == [sanitize_anki_deck_name("Child:Deck")]
    assert root_deck_json["note_models"] == [{"model": "root"}]

    assert json.loads(notes_json_path.read_text(encoding="utf8")) == root_notes

    child_directory = export_dir / sanitize_anki_deck_name("Child:Deck")
    assert child_directory.exists()

    child_deck_json = json.loads((child_directory / "deck.json").read_text(encoding="utf8"))
    assert "notes" not in child_deck_json
    assert child_deck_json["children"] == []
    assert child_deck_json["deck_configurations"] == [{"child": "config"}]

    assert json.loads((child_directory / "notes.json").read_text(encoding="utf8")) == child_notes
    assert exported_tree["exporter"].last_exported_count == 2


def test_importer_expands_hierarchical_exports(exported_tree):
    export_dir: Path = exported_tree["export_dir"]
    root_notes = exported_tree["root_notes"]
    child_notes = exported_tree["child_notes"]

    importer = AnkiJsonImporter(MagicMock())
    deck_json = importer.read_deck(export_dir, export_dir / "deck.json")

    assert deck_json["notes"] == root_notes
    assert len(deck_json["children"]) == 1

    child_json = deck_json["children"][0]
    assert child_json["name"] == "Child:Deck"
    assert child_json["notes"] == child_notes
    assert child_json["children"] == []
