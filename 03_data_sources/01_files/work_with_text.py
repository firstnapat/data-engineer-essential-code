"""
Work with a TEXT data source.   read -> inspect -> clean

Text has no schema, so 'clean' means parsing the structured bits out of free text.
"""
import os
import re
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")


def read(path: str) -> list[str]:
    with open(path, encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def inspect(lines: list[str]) -> None:
    print(f"[inspect] {len(lines)} lines, {sum(len(l) for l in lines)} chars")
    print("first 3 lines:")
    for line in lines[:3]:
        print(f"  {line!r}")


def clean(lines: list[str]) -> pd.DataFrame:
    """Parse the '1. Bangkok:  520,000 THB' rows into a tidy table."""
    pattern = re.compile(r"^\s*\d+\.\s*(?P<region>[\w ]+?):\s*(?P<revenue>[\d,]+)\s*THB")
    rows = [
        {"region": m.group("region").strip(), "revenue": int(m.group("revenue").replace(",", ""))}
        for line in lines if (m := pattern.match(line))
    ]
    return pd.DataFrame(rows)


if __name__ == "__main__":
    lines = read(os.path.join(DATASETS, "sample.txt"))
    inspect(lines)
    df = clean(lines)
    print("\n[clean] parsed regions:")
    print(df)
