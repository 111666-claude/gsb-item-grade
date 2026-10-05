import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grading.parser import parse_item  # noqa: E402


class ParseItemTest(unittest.TestCase):
    def test_reads_id_and_field(self):
        item = parse_item("item_id=sword;atk=10")
        self.assertEqual(item["id"], "sword")
        self.assertEqual(item["fields"]["atk"], 10)

    def test_ignores_empty_parts(self):
        item = parse_item("item_id=sword;;atk=10;")
        self.assertEqual(len(item["fields"]), 1)

    def test_ignores_unknown_affix(self):
        item = parse_item("item_id=charm;lucky=5;atk=1")
        self.assertNotIn("lucky", item["fields"])
        self.assertEqual(item["fields"]["atk"], 1)
        self.assertTrue(item["valid"])

    def test_bad_number_marks_invalid(self):
        item = parse_item("item_id=broken;atk=abc")
        self.assertFalse(item["valid"])

    def test_rarity_out_of_range_marks_invalid(self):
        self.assertFalse(parse_item("item_id=a;rarity=0")["valid"])
        self.assertFalse(parse_item("item_id=a;rarity=6")["valid"])

    def test_rarity_boundaries_are_valid(self):
        self.assertTrue(parse_item("item_id=a;rarity=1")["valid"])
        self.assertTrue(parse_item("item_id=a;rarity=5")["valid"])

    def test_missing_rarity_is_valid(self):
        self.assertTrue(parse_item("item_id=a;atk=1")["valid"])


if __name__ == "__main__":
    unittest.main()
