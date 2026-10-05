"""装备行解析：item_id=sword;atk=10;crit=5;rarity=3。

口径：未知词条忽略；数值解析失败或 rarity 不在 1 到 5 之间时整件判 invalid。
"""

KNOWN_KEYS = {"atk", "crit", "def", "rarity"}


def parse_item(line):
    """解析一行装备，未知词条忽略，非法数值或越界 rarity 标记 invalid。"""
    item_id = ""
    fields = {}
    valid = True
    for part in line.strip().split(";"):
        if not part:
            continue
        key, _, value = part.partition("=")
        if key == "item_id":
            item_id = value
            continue
        if key not in KNOWN_KEYS:
            continue
        try:
            number = int(value)
        except ValueError:
            valid = False
            continue
        if key == "rarity" and not 1 <= number <= 5:
            valid = False
            continue
        fields[key] = number
    return {"id": item_id, "fields": fields, "valid": valid}
