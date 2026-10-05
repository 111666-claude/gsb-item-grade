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


if __name__ == "__main__":
    unittest.main()


class GradeRuleTest(unittest.TestCase):
    def test_exact_thresholds_take_higher_tier(self):
        grader = Grader()
        self.assertEqual(grader.grade(parse_item("item_id=s;atk=10")), "S")
        self.assertEqual(grader.grade(parse_item("item_id=a;atk=7")), "A")
        self.assertEqual(grader.grade(parse_item("item_id=b;atk=4")), "B")
        self.assertEqual(grader.grade(parse_item("item_id=c;atk=3;crit=1")), "C")

    def test_rarity_bonus_added(self):
        grader = Grader()
        grader.grade(parse_item("item_id=sword;atk=10;rarity=3"))
        self.assertEqual(grader.seen["sword"], 110)

    def test_unknown_field_scores_zero(self):
        grader = Grader()
        grader.grade(parse_item("item_id=charm;lucky=5"))
        self.assertEqual(grader.seen["charm"], 0)

    def test_invalid_item_is_not_scored(self):
        grader = Grader()
        self.assertEqual(grader.grade(parse_item("item_id=broken;atk=abc")), "invalid")
        self.assertNotIn("broken", grader.seen)

    def test_duplicate_id_returns_first_tier_and_skips_work(self):
        grader = Grader()
        self.assertEqual(grader.grade(parse_item("item_id=sword;atk=10")), "S")
        work_after_first = grader.work_count()
        self.assertEqual(grader.grade(parse_item("item_id=sword;atk=1")), "S")
        self.assertEqual(grader.work_count(), work_after_first)

    def test_work_scales_with_distinct_items_only(self):
        grader = Grader()
        for index in range(3000):
            grader.grade(parse_item("item_id=i-%d;atk=1" % index))
        self.assertEqual(grader.work_count(), 3000)
