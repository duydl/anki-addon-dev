import json
from pathlib import Path
from typing import Callable, List

from .anki_exporter import AnkiJsonExporter
from ..representation.deck import Deck
from ..representation import deck_initializer
from ..utils.constants import (
    DECK_FILE_EXTENSION,
    NOTES_FILE_NAME,
    NOTES_HTML_FILE_NAME,
    METADATA_FILE_NAME,
)
from ..utils.filesystem.name_sanitizer import sanitize_anki_deck_name
from ..utils.note_html import notes_to_html


class HierarchicalJsonExporter(AnkiJsonExporter):
    """Exporter that stores each deck in its own directory."""

    def __init__(
        self,
        collection,
        config,
        deck_name_sanitizer: Callable[[str], str] = sanitize_anki_deck_name,
        deck_file_name: str = "deck",
    ):
        super().__init__(collection, config, deck_name_sanitizer, deck_file_name)

    def export_to_directory(
        self,
        deck,
        output_dir=Path("."),
        copy_media: bool = True,
        create_deck_subdirectory: bool = True,
    ) -> Path:
        deck_directory = output_dir
        if create_deck_subdirectory:
            deck_directory = output_dir.joinpath(self.deck_name_sanitizer(deck.name))
            deck_directory.mkdir(parents=True, exist_ok=True)

        deck = deck_initializer.from_collection(self.collection, deck.name)

        self.note_sorter.sort_deck(deck)
        self.last_exported_count = deck.get_note_count()

        self._export_deck_recursive(deck, deck_directory)

        self._save_changes(deck)

        if copy_media:
            self._copy_media(deck, deck_directory)

        self._export_viewer(deck_directory, deck, self.deck_file_name)

        return deck_directory

    def _export_deck_recursive(self, deck, deck_directory: Path) -> None:
        deck_directory.mkdir(parents=True, exist_ok=True)

        deck_dict = json.loads(
            json.dumps(
                deck,
                default=Deck.default_json,
                sort_keys=True,
                ensure_ascii=False,
            )
        )

        notes = deck_dict.pop("notes", [])
        metadata = {}
        note_models = deck_dict.pop("note_models", None)
        if note_models:
            metadata["note_models"] = note_models
        children_payloads: List = deck_dict.pop("children", [])

        sanitized_children = []
        for index, child in enumerate(deck.children):
            child_payload = children_payloads[index] if index < len(children_payloads) else {}
            child_name = child_payload.get("name") or child.anki_dict.get("name")
            sanitized_child_name = self.deck_name_sanitizer(child_name)
            sanitized_children.append(sanitized_child_name)

            child_directory = deck_directory.joinpath(sanitized_child_name)
            self._export_deck_recursive(child, child_directory)

        deck_dict["children"] = sanitized_children

        deck_path = deck_directory.joinpath(self.deck_file_name).with_suffix(DECK_FILE_EXTENSION)
        with deck_path.open(mode="w", encoding="utf8") as deck_file:
            deck_file.write(
                json.dumps(
                    deck_dict,
                    sort_keys=True,
                    indent=4,
                    ensure_ascii=False,
                )
            )

        notes_path = deck_directory.joinpath(NOTES_FILE_NAME)
        with notes_path.open(mode="w", encoding="utf8") as notes_file:
            notes_file.write(
                json.dumps(
                    notes,
                    sort_keys=True,
                    indent=4,
                    ensure_ascii=False,
                )
            )

        notes_html_path = deck_directory.joinpath(NOTES_HTML_FILE_NAME)
        notes_html_path.write_text(
            notes_to_html(notes, metadata.get("note_models"), deck_dict.get("name")),
            encoding="utf8",
        )

        metadata_path = deck_directory.joinpath(METADATA_FILE_NAME)
        if metadata:
            with metadata_path.open(mode="w", encoding="utf8") as metadata_file:
                metadata_file.write(
                    json.dumps(
                        metadata,
                        sort_keys=True,
                        indent=4,
                        ensure_ascii=False,
                    )
                )
        elif metadata_path.exists():
            metadata_path.unlink()

    def _export_viewer(self, deck_directory: Path, deck, deck_file_name) -> None:
        viewer_path = Path(__file__).parent.joinpath("viewer")
        for file_name in ["index.html", "viewer.css", "viewer.js"]:
            src = viewer_path.joinpath(file_name)
            dst = deck_directory.joinpath(file_name)
            if src.exists(): # Should exist as we created them
                dst.write_bytes(src.read_bytes())

        # Generate manifest
        manifest = self._generate_manifest(deck, deck_file_name)
        manifest_js = f"window.deckManifest = {json.dumps(manifest, indent=4)};"
        deck_directory.joinpath("manifest.js").write_text(manifest_js, encoding="utf-8")

    def _generate_manifest(self, deck, deck_file_name) -> dict:
        # Recursive function to build manifest
        # deck structure is already akin to what we need, but we need file paths relative to root

        def build_node(node, current_path=""):
             # node is a Deck object
             # current_path is the relative path from root to this deck's folder

             node_data = {
                 "name": node.anki_dict["name"].split("::")[-1],
                 "deckPath": f"{current_path}{deck_file_name}.json",
                 "notesPath": f"{current_path}{NOTES_FILE_NAME}",
                 "children": []
             }
             
             # Check for models
             models_path = f"{current_path}{METADATA_FILE_NAME}"
             node_data["modelsPath"] = models_path

             for child in node.children:
                 child_dirname = self.deck_name_sanitizer(child.anki_dict["name"].split("::")[-1])
                 child_rel_path = f"{current_path}{child_dirname}/"
                 
                 child_node = build_node(child, child_rel_path)
                 node_data["children"].append(child_node)

             return node_data

        return build_node(deck)

