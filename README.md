# EDGAR Schedule of Investments Extractor

A parsing layer over edgartools for converting the Schedule of Investments from SEC EDGAR filings into CSV format.

## Features

- Automatically downloads 10-Q and 10-K filings from SEC EDGAR
- Extracts Schedule of Investments sections
- Converts data to CSV format
- Supports batch processing of multiple companies
- Creates organized output directory structure
- Automatically zips results for easy sharing

## Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)

1. Clone this repository (or download files):
```bash
git clone https://github.com/hrbatra/sec-schedule-parser.git
cd sec-schedule-parser
```

2. Install edgartools:
```bash
pip edgartools==3.1.2
```

## Usage
(or follow usage_example.ipynb as an alternative)

1. Open `edgar_extractor.py` and update the `USER_EMAIL` variable with your email address:
```python
USER_EMAIL = "your.email@domain.com"
```

2. (Optional) Modify the `SCHEMA` dictionary to track different companies:
```python
# downloads the latest N filings given for each form
SCHEMA = {
    "GSBD": {"10-Q": 4, "10-K": 1},  # Goldman Sachs BDC
    "OBDC": {"10-Q": 4, "10-K": 1},  # Blue Owl BDC
    "BBDC": {"10-Q": 4, "10-K": 1},  # Barings BDC
    "BCSF": {"10-Q": 4, "10-K": 1}   # Bain Capital Specialty Finance
}
```

3. Run the script:
```bash
python edgar_extractor.py
```

## Output

The script creates an organized directory structure:
```
output/
├── Company_Name_1/
│   ├── TICKER_10-Q_2024-02-15.csv
│   ├── TICKER_10-Q_2023-11-15.csv
│   └── TICKER_10-K_2023-12-31.csv
├── Company_Name_2/
│   └── ...
└── ...
```

All results are automatically zipped into `output.zip`.

## Configuration

You can modify the following settings in `edgar_extractor.py`:

- `USER_EMAIL`: Your email address (required by SEC EDGAR)
- `OUTPUT_DIR`: Directory where files will be saved
- `SCHEMA`: Dictionary specifying companies and filings to process
