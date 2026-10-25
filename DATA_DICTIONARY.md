# Data dictionary

Each CSV row describes one country and one measure for one reporting year.

| Field | Meaning |
| --- | --- |
| country | Country name as written by the reporting source |
| year | Reporting year, as an integer |
| measure | `production`, `yield`, or `production_change` in the initial data |
| value | Numeric value as published |
| unit | Unit printed in the source |
| source | Direct URL to the original release |
| source_date | Release date in ISO format when known |

## Comparison rules

A rank is meaningful only for rows with the same year, measure, and unit. Production and yield are separate measures. A percentage change is not a production amount. National reporting definitions may differ, so comparisons need a source review before they are described as fully comparable.
