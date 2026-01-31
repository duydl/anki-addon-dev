
import json
import unittest
from xml.etree import ElementTree as ET

from crowd_anki.utils import note_html


class NoteHtmlTest(unittest.TestCase):
    def setUp(self):
        self.notes = [
            {
                "fields": ["Field1", "Field2"],
                "tags": ["tag1", "tag2"],
                "guid": "test_guid",
                "note_model_uuid": "test_model_uuid",
                "extra_data": {"nested": "value"}
            }
        ]
        self.note_models = [
            {
                "crowdanki_uuid": "test_model_uuid",
                "flds": [{"name": "Front"}, {"name": "Back"}]
            }
        ]

    def test_round_trip(self):
        html = note_html.notes_to_html(self.notes, self.note_models)
        parsed_notes = note_html.notes_from_html(html)

        self.assertEqual(len(parsed_notes), 1)
        parsed_note = parsed_notes[0]

        self.assertEqual(parsed_note["fields"], self.notes[0]["fields"])
        self.assertEqual(parsed_note["tags"], self.notes[0]["tags"])
        self.assertEqual(parsed_note["guid"], self.notes[0]["guid"])
        self.assertEqual(parsed_note["note_model_uuid"], self.notes[0]["note_model_uuid"])
        self.assertEqual(parsed_note["extra_data"], self.notes[0]["extra_data"])

    def test_legacy_format_parsing(self):
        legacy_html = """
        <html>
            <cards>
                <card guid="legacy_guid">
                    <field>Legacy Field 1</field>
                    <tags>legacy_tag</tags>
                </card>
            </cards>
        </html>
        """
        parsed_notes = note_html.notes_from_html(legacy_html)
        self.assertEqual(len(parsed_notes), 1)
        self.assertEqual(parsed_notes[0]["guid"], "legacy_guid")
        self.assertEqual(parsed_notes[0]["fields"], ["Legacy Field 1"])
        self.assertEqual(parsed_notes[0]["tags"], ["legacy_tag"])

    def test_html_structure(self):
        html = note_html.notes_to_html(self.notes, self.note_models)
        root = ET.fromstring(html)
        
        # Check for new structure
        cards = root.find(".//div[@class='cards']")
        self.assertIsNotNone(cards)
        
        card = cards.find("div[@class='card']")
        self.assertIsNotNone(card)
        self.assertEqual(card.get("guid"), "test_guid")
        
        fields = card.findall("div[@class='field']")
        self.assertEqual(len(fields), 2)
        self.assertEqual(fields[0].get("name"), "Front")
        
        tags = card.find("div[@class='tags']")
        self.assertIsNotNone(tags)
        self.assertEqual(tags.text, "tag1 tag2")
