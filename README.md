# Honey and Hives

A cited dataset and Python command line tool for comparing honey production and managed hive statistics.

## What is here

- `data/observations.csv` stores a small set of figures from the USDA 2025 Honey report.
- `src/rankings.py` validates observations and ranks countries within one year, measure, and unit.
- `DATA_DICTIONARY.md` defines the record fields and comparison rules.
- `SOURCES.md` links to official statistics and explains the limits of the current data.

The initial data records United States honey production of 116 million pounds in 2025, a yield of 48.0 pounds per producing colony, and a 14 percent decline in production from 2024. These figures are rounded as published by USDA. The initial table does not yet support a world ranking because it contains one country.

## Run

```sh
python3 src/rankings.py data/observations.csv --year 2025 --measure production
```

Use `--measure yield` or `--measure production_change` to view the other recorded measures. Values are compared only when year, measure, and unit match.

## Adding observations

Add one row per country, year, measure, and unit. Keep the original unit, identify the source, and record the source release date. Do not estimate missing values or combine different definitions. Add Central Asian country records when a comparable official source and year are available.

## License

Original code and documentation are under the MIT License. Data records retain the terms of their issuing source.
