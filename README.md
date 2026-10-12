# MP1: End-to-End Data Pipeline

A command-line data pipeline that loads, validates, cleans, and saves tabular data. The pipeline reads an input file (CSV, JSON, or YAML) and a YAML configuration file, then runs the data through a sequence of stages controlled entirely by the configuration. Data first flows into the **loaders**, which read the file into a pandas DataFrame; next the **validator** checks that required columns exist and removes rows with invalid numeric values; then the **processor** cleans the data by removing duplicate rows, dropping missing values, and filtering outliers using the IQR method; finally the **output** module saves the cleaned DataFrame as a CSV file. The project is organized so that the command-line logic lives in `pipeline.py` at the root, all reusable modules live under `src/`, and the processing settings live in `config/config.yaml`, which means the pipeline can clean different datasets by editing the configuration rather than the code.

## Project Structure

- `pipeline.py` — coordinates the end-to-end pipeline and handles command-line arguments.
- `src/data_loaders.py` — loads CSV, JSON, and YAML files into Python objects.
- `src/data_validator.py` — checks required columns and removes invalid numeric values.
- `src/data_processor.py` — removes duplicates, handles missing values, and removes outliers.
- `src/data_output.py` — saves the cleaned DataFrame to a CSV file.
- `src/utils.py` — sets up logging and validates input file paths.
- `config/config.yaml` — controls which validation and processing steps run.

## Example

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output (abbreviated):

```text
INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
INFO     __main__ — Validation complete: 100 → 98 rows
INFO     __main__ — Processing complete: 98 → 92 rows
INFO     __main__ — Saved cleaned data to output/clean.csv

Cleaning report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```