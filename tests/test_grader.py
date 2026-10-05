import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grading.grader import Grader  # noqa: E402
from grading.parser import parse_item  # noqa: E402


class GradeTest(unittest.TestCase):
    def test_low_score_is_c(self):
        grader = Grader()
        self.assertEqual(grader.grade(parse_item("item_id=a;atk=1")), "C")

    def test_high_score_is_s(self):
        grader = Grader()
        self.assertEqual(grader.grade(parse_item("item_id=a;atk=20")), "S")

    def test_work_starts_at_zero(self):
        self.assertEqual(Grader().work_count(), 0)

    def test_threshold_boundary(self):
        grader = Grader()
        self.assertEqual(grader.grade(parse_item("item_id=a;atk=10")), "S")
        self.assertEqual(grader.grade(parse_item("item_id=b;atk=7")), "A")
        self.assertEqual(grader.grade(parse_item("item_id=c;atk=4")), "B")
        self.assertEqual(grader.grade(parse_item("item_id=d;atk=9")), "A")
        self.assertEqual(grader.grade(parse_item("item_id=e;atk=6")), "B")
        self.assertEqual(grader.grade(parse_item("item_id=f;atk=3")), "C")

    def test_rarity_bonus(self):
        grader = Grader()
        grader.grade(parse_item("item_id=a;atk=10;rarity=3"))
        self.assertEqual(grader.seen["a"]["score"], 110)
        grader.grade(parse_item("item_id=b;atk=10;rarity=1"))
        self.assertEqual(grader.seen["b"]["score"], 100)

    def test_unknown_affix_ignored(self):
        grader = Grader()
        grader.grade(parse_item("item_id=charm;lucky=5"))
        self.assertEqual(grader.seen["charm"]["score"], 0)
        self.assertEqual(grader.grade(parse_item("item_id=charm;lucky=5")), "C")

    def test_invalid_parse(self):
        grader = Grader()
        self.assertEqual(grader.grade(parse_item("item_id=broken;atk=abc")), "invalid")
        self.assertEqual(grader.seen["broken"]["tier"], "invalid")

    def test_invalid_rarity(self):
        grader = Grader()
        self.assertEqual(grader.grade(parse_item("item_id=a;rarity=6")), "invalid")
        self.assertEqual(grader.grade(parse_item("item_id=a;rarity=0")), "invalid")

    def test_idempotent(self):
        grader = Grader()
        self.assertEqual(grader.grade(parse_item("item_id=a;atk=10")), "S")
        self.assertEqual(grader.grade(parse_item("item_id=a;atk=1")), "S")
        self.assertEqual(grader.work_count(), 1)

    def test_work_scales_linearly(self):
        grader = Grader()
        for index in range(3000):
            grader.grade(parse_item("item_id=i-%d;atk=1" % index))
        self.assertEqual(grader.work_count(), 3000)

    def test_work_does_not_rescan(self):
        grader = Grader()
        for index in range(3000):
            grader.grade(parse_item("item_id=i-%d;atk=1" % index))
        for index in range(3000):
            grader.grade(parse_item("item_id=i-%d;atk=1" % index))
        self.assertEqual(grader.work_count(), 3000)


if __name__ == "__main__":
    unittest.main()
