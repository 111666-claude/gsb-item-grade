# item-grade

装备评级：装备行按 `item_id=..;词条=值` 解析，词条加权求和后分档，只用 Python 标准库。

```
python3 grade.py --sample tier
python3 grade.py --sample rarity
python3 grade.py --sample unknown
python3 grade.py --sample parse
python3 grade.py --sample dup
python3 grade.py --sample work
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **解析**：字段用分号分隔、键值用等号；未知词条忽略；数值解析失败或 `rarity` 不在 1 到 5 之间时，
  整件装备判为 `invalid`，不再计分与分档。
- **计分**：分数等于各词条值乘权重之和，再加 `(rarity - 1) × 5` 的品质加成；权重表为
  `atk=10`、`crit=8`、`def=5`。
- **分档**：分数不小于 100 为 `S`，不小于 70 为 `A`，不小于 40 为 `B`，否则 `C`；正好等于阈值算更高一档。
- **幂等**：同一个 `item_id` 只评级一次，重复调用返回上一次的档位。
- **代价**：评级不许全扫已评过的装备，`work_count()` 不随装备数乘评级次数增长；10 万件装备每秒 10 万次评级。

## 输出契约（不改格式）

```
tier=..
score=..
work=..
```

## 目录

```
grade.py                命令行入口（顶层脚本）
grading/parser.py       装备行解析
grading/grader.py       计分与分档
tests/test_parser.py    解析用例
tests/test_grader.py    评级用例
```
