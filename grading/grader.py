"""装备评级：词条加权求和再分档。

口径：分数 = 各词条值乘权重之和 + (rarity - 1) * 5；分数不小于 100 为 S、
不小于 70 为 A、不小于 40 为 B，否则 C；同一 item_id 只评级一次；评级不做全扫。
"""

WEIGHTS = {"atk": 10, "crit": 8, "def": 5}
TIERS = (("S", 100), ("A", 70), ("B", 40))


def tier_for(score):
    """分数分档：阈值含等号，正好等于阈值算更高一档。"""
    for name, need in TIERS:
        if score >= need:
            return name
    return "C"


class Grader:
    """评级台账：seen 按 item_id 缓存上一次的分数与档位。"""

    def __init__(self):
        self.seen = {}
        self.work = 0

    def grade(self, item):
        """返回装备档位，O(1)：命中缓存直接返回，不重算、不全扫已评装备。"""
        item_id = item["id"]
        if item_id in self.seen:
            return self.seen[item_id]["tier"]
        self.work += 1
        if not item.get("valid", True):
            self.seen[item_id] = {"score": None, "tier": "invalid"}
            return "invalid"
        fields = item["fields"]
        score = 0
        for key, value in fields.items():
            if key == "rarity":
                continue
            score += value * WEIGHTS[key]
        score += (fields.get("rarity", 1) - 1) * 5
        tier = tier_for(score)
        self.seen[item_id] = {"score": score, "tier": tier}
        return tier

    def work_count(self):
        return self.work
