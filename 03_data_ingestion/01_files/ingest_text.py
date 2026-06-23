"""
Ingest a plain-text report file.

Text files have no schema, so ingestion means: read lines -> parse the parts we
care about -> return structured rows (a DataFrame).
Pattern: read -> parse -> structure
"""
import os
import re
import pandas as pd

DATASETS = os.path.join(os.path.dirname(__file__), "../../datasets")


def read_lines(filepath: str) -> list[str]:
    """Read a text file into a list of lines (newline stripped)."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    print(f"[read] {len(lines)} raw lines from {os.path.basename(filepath)}")
    return lines


def parse_regions(lines: list[str]) -> pd.DataFrame:
    """Extract '1. Bangkok:  520,000 THB' style rows into a structured table."""
    pattern = re.compile(r"^\s*\d+\.\s*(?P<region>[\w ]+?):\s*(?P<revenue>[\d,]+)\s*THB")
    records = []
    for line in lines:
        m = pattern.match(line)
        if m:
            records.append({
                "region": m.group("region").strip(),
                "revenue": int(m.group("revenue").replace(",", "")),
            })
    df = pd.DataFrame(records)
    print(f"[parse] {len(df)} region rows extracted")
    return df


if __name__ == "__main__":
    src = os.path.join(DATASETS, "sample.txt")
    lines = read_lines(src)
    df = parse_regions(lines)

    print("\n--- Parsed Regions ---")
    print(df)
    print(f"\nTotal extracted revenue: {df['revenue'].sum():,} THB")
