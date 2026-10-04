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


if __name__ == "__main__":
    unittest.main()
