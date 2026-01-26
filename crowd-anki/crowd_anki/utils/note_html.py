from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Optional
from xml.dom import minidom
from xml.etree import ElementTree as ET

from .constants import UUID_FIELD_NAME


ATTRIBUTE_KEYS = ("guid", "note_model_uuid")
FIELD_FALLBACK_TEMPLATE = "Field {index}"


def _field_names_by_model(note_models: Optional[Iterable[Dict[str, Any]]]) -> Dict[str, List[str]]:
    if not note_models:
        return {}

    mapping: Dict[str, List[str]] = {}
    for model in note_models:
        if not isinstance(model, dict):
            continue

        uuid = (
            model.get(UUID_FIELD_NAME)
            or model.get("crowdanki_uuid")
            or model.get("id")
        )
        if not uuid:
            continue

        field_names: List[str] = []
        fields = model.get("flds", [])
        if isinstance(fields, list):
            for index, field in enumerate(fields, start=1):
                if isinstance(field, dict):
                    name = field.get("name")
                else:
                    name = None
                field_names.append(name or FIELD_FALLBACK_TEMPLATE.format(index=index))

        mapping[str(uuid)] = field_names

    return mapping


def notes_to_html(
    notes: Iterable[Dict[str, Any]],
    note_models: Optional[Iterable[Dict[str, Any]]] = None,
    deck_name: Optional[str] = None,
) -> str:
    """Serialize notes into a human-friendly HTML representation."""

    html_root = ET.Element("html")
    head = ET.SubElement(html_root, "head")
    ET.SubElement(head, "meta", attrib={"charset": "utf-8"})
    title = ET.SubElement(head, "title")
    title.text = "CrowdAnki Notes"

    body = ET.SubElement(html_root, "body")
    cards_container = ET.SubElement(body, "cards")
    if deck_name:
        cards_container.set("deck", str(deck_name))

    field_names_map = _field_names_by_model(note_models)

    for note in notes:
        if not isinstance(note, dict):
            continue

        card_element = ET.SubElement(cards_container, "card")

        for key in ATTRIBUTE_KEYS:
            value = note.get(key)
            if value is not None:
                card_element.set(key, str(value))

        fields = note.get("fields", [])
        if not isinstance(fields, list):
            fields = []

        model_uuid = card_element.get("note_model_uuid")
        model_field_names = field_names_map.get(model_uuid or "", [])

        for index, field_value in enumerate(fields, start=1):
            field_element = ET.SubElement(card_element, "field")
            field_name = (
                model_field_names[index - 1]
                if index - 1 < len(model_field_names)
                else FIELD_FALLBACK_TEMPLATE.format(index=index)
            )
            field_element.set("name", field_name)
            field_element.text = "" if field_value is None else str(field_value)

        tags = note.get("tags")
        if isinstance(tags, list):
            tags_element = ET.SubElement(card_element, "tags")
            tags_element.text = " ".join(str(tag) for tag in tags if tag is not None)

        for key, value in note.items():
            if key in ATTRIBUTE_KEYS or key in {"fields", "tags"}:
                continue

            extra_element = ET.SubElement(card_element, "extra", attrib={"key": str(key)})
            extra_element.text = json.dumps(value, ensure_ascii=False)

    rough_string = ET.tostring(html_root, encoding="utf-8")
    parsed = minidom.parseString(rough_string)
    # minidom adds an XML declaration; keep it for readability.
    return parsed.toprettyxml(indent="  ")


def notes_from_html(html_text: str) -> List[Dict[str, Any]]:
    """Parse notes stored in :func:`notes_to_html` format."""

    if not html_text.strip():
        return []

    try:
        root = ET.fromstring(html_text)
    except ET.ParseError:
        return []

    cards_container = root.find(".//cards")
    if cards_container is None:
        return []

    parsed_notes: List[Dict[str, Any]] = []

    for card_element in cards_container.findall("card"):
        note: Dict[str, Any] = {}

        for key in ATTRIBUTE_KEYS:
            value = card_element.get(key)
            if value is not None:
                note[key] = value

        fields: List[str] = []
        for field_element in card_element.findall("field"):
            fields.append(field_element.text or "")

        if fields:
            note["fields"] = fields

        tags_element = card_element.find("tags")
        if tags_element is not None:
            text = tags_element.text or ""
            tags = [tag for tag in text.split(" ") if tag]
            note["tags"] = tags

        for extra_element in card_element.findall("extra"):
            key = extra_element.get("key")
            if not key:
                continue
            data = extra_element.text or ""
            try:
                value = json.loads(data)
            except json.JSONDecodeError:
                value = data
            note[key] = value

        note.setdefault("fields", [])
        note.setdefault("tags", [])

        parsed_notes.append(note)

    return parsed_notes

