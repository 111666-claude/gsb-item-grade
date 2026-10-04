"""装备行解析：item_id=sword;atk=10;crit=5;rarity=3。

缺陷：未知词条照收、数值非法当 0 继续、rarity 不校验范围。
"""


def parse_item(line):
    """解析一行装备。缺陷：未知键照收、非法数字当 0。"""
    item_id = ""
    fields = {}
    for part in line.strip().split(";"):
        if not part:
            continue
        key, _, value = part.partition("=")
        if key == "item_id":
            item_id = value
            continue
        try:
            number = int(value)
        except ValueError:
            number = 0
        fields[key] = number
    return {"id": item_id, "fields": fields}
