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
