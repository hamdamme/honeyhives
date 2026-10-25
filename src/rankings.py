"""Validate and rank honey observations from a cited CSV file."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

REQUIRED_COLUMNS = {
    "country",
    "year",
    "measure",
    "value",
    "unit",
    "source",
    "source_date",
}


@dataclass(frozen=True)
class Observation:
    country: str
    year: int
    measure: str
    value: float
    unit: str
    source: str
    source_date: str


def read_observations(stream: TextIO) -> list[Observation]:
    reader = csv.DictReader(stream)
    columns = set(reader.fieldnames or ())
    missing = REQUIRED_COLUMNS - columns
    if missing:
        raise ValueError("Missing CSV columns: " + ", ".join(sorted(missing)))

    observations: list[Observation] = []
    seen: set[tuple[str, int, str, str]] = set()
    for line_number, row in enumerate(reader, start=2):
        country = (row.get("country") or "").strip()
        measure = (row.get("measure") or "").strip()
        unit = (row.get("unit") or "").strip()
        source = (row.get("source") or "").strip()
        source_date = (row.get("source_date") or "").strip()
        if not all((country, measure, unit, source, source_date)):
            raise ValueError(f"Line {line_number}: text fields cannot be blank")
        try:
            year = int(row["year"])
            value = float(row["value"])
        except (TypeError, ValueError) as error:
            raise ValueError(f"Line {line_number}: year and value must be numeric") from error
        if year < 1900 or year > 2200:
            raise ValueError(f"Line {line_number}: year is outside the accepted range")
        key = (country.casefold(), year, measure, unit)
        if key in seen:
            raise ValueError(f"Line {line_number}: duplicate country and measure record")
        seen.add(key)
        observations.append(
            Observation(country, year, measure, value, unit, source, source_date)
        )
    return observations


def rank_observations(
    observations: list[Observation],
    year: int,
    measure: str,
) -> list[Observation]:
    selected = [
        item
        for item in observations
        if item.year == year and item.measure == measure
    ]
    units = {item.unit for item in selected}
    if len(units) > 1:
        raise ValueError("Selected observations use different units")
    return sorted(selected, key=lambda item: (-item.value, item.country.casefold()))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--measure", required=True)
    args = parser.parse_args()

    try:
        with args.csv_file.open("r", encoding="utf-8", newline="") as stream:
            observations = read_observations(stream)
        ranked = rank_observations(observations, args.year, args.measure)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if not ranked:
        print("No matching observations.")
        return 0

    print(f"Rank  Country  Value  Unit")
    for position, item in enumerate(ranked, start=1):
        print(f"{position}  {item.country}  {item.value:g}  {item.unit}")
    print("Source URLs are recorded in the input file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
