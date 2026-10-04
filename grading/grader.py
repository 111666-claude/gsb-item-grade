"""装备评级：词条加权求和再分档。

缺陷：分档阈值用开区间、不算品质加成、未知词条按权重 1 计、同一 item_id 重复评级会重算、
每次评级全扫已评过的装备。
"""

WEIGHTS = {"atk": 10, "crit": 8, "def": 5}
TIERS = (("S", 100), ("A", 70), ("B", 40))


class Grader:
    """评级台账。"""

    def __init__(self):
        self.seen = {}
        self.work = 0

    def grade(self, item):
        """返回装备档位。缺陷：阈值开区间、不加品质、未知词条按 1 计、重复 id 重算、全扫。"""
        self.work += len(self.seen)
        score = 0
        for key, value in item["fields"].items():
            if key == "rarity":
                continue
            score += value * WEIGHTS.get(key, 1)
        self.seen[item["id"]] = score
        for name, need in TIERS:
            if score > need:
                return name
        return "C"

    def work_count(self):
        return self.work
