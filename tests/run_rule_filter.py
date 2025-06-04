# test_rule_filter.py

from src.rule_filter import apply_rules

tests = [
    "High‑quality printer toner, black ink",
    "Steel beam for construction",
    "Unknown item description"
]

for desc in tests:
    result = apply_rules(desc)
    print(f"DESC: {desc!r}  →  {result}")
