"""装备评级：词条加权求和加品质加成再分档，同一 item_id 只评级一次。"""

WEIGHTS = {"atk": 10, "crit": 8, "def": 5}
TIERS = (("S", 100), ("A", 70), ("B", 40))


class Grader:
    """评级台账：按 item_id 缓存分数与档位，评级为 O(1)。"""

    def __init__(self):
        self.seen = {}
        self.tiers = {}
        self.work = 0

    def grade(self, item):
        """返回装备档位；invalid 返回 "invalid"，重复 id 返回上次档位。"""
        item_id = item["id"]
        if item_id in self.tiers:
            return self.tiers[item_id]
        self.work += 1
        if not item.get("valid", True):
            self.tiers[item_id] = "invalid"
            return "invalid"
        fields = item["fields"]
        score = sum(value * WEIGHTS[key] for key, value in fields.items() if key in WEIGHTS)
        score += (fields.get("rarity", 1) - 1) * 5
        self.seen[item_id] = score
        for name, need in TIERS:
            if score >= need:
                self.tiers[item_id] = name
                return name
        self.tiers[item_id] = "C"
        return "C"

    def work_count(self):
        return self.work
