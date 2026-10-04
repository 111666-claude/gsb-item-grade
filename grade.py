"""装备评级入口：python3 grade.py --sample <名>。"""

import argparse

from grading.grader import Grader
from grading.parser import parse_item


def build_parser():
    parser = argparse.ArgumentParser(prog="item-grade", description="装备评级")
    parser.add_argument("--sample", default="tier", help="tier / rarity / unknown / parse / dup / work")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    grader = Grader()
    if args.sample == "tier":
        # atk 权重 10，攻击 10 点正好 100 分。
        item = parse_item("item_id=sword;atk=10")
        print("tier=%s" % grader.grade(item))
    elif args.sample == "rarity":
        item = parse_item("item_id=sword;atk=10;rarity=3")
        grader.grade(item)
        print("score=%d" % grader.seen["sword"])
    elif args.sample == "unknown":
        item = parse_item("item_id=charm;lucky=5")
        grader.grade(item)
        print("score=%d" % grader.seen["charm"])
    elif args.sample == "parse":
        item = parse_item("item_id=broken;atk=abc")
        print("tier=%s" % grader.grade(item))
    elif args.sample == "dup":
        grader.grade(parse_item("item_id=sword;atk=10"))
        print("tier=%s" % grader.grade(parse_item("item_id=sword;atk=1")))
    elif args.sample == "work":
        for index in range(3000):
            grader.grade(parse_item("item_id=i-%d;atk=1" % index))
        print("work=%d" % grader.work_count())
    else:
        raise SystemExit("需要 --sample tier|rarity|unknown|parse|dup|work")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
