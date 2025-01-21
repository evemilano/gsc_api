# Google Search Console Data Aggregator

## Overview
`gsc.py` is a Python script designed to authenticate with Google Search Console, retrieve search analytics data, and generate comprehensive reports. The script processes queries, clicks, impressions, CTR, and position metrics, then saves the results in Excel and CSV formats.

## Features
- Authenticates with Google Search Console.
- Retrieves search analytics data for a specific property and date range.
- Aggregates metrics such as:
  - Total clicks and impressions.
  - CTR as a percentage.
  - Average position (weighted by impressions).
- Outputs the processed data into:
  - Excel (`search_analytics_data.xlsx`)
  - CSV (`search_analytics_data.csv`)

## Prerequisites
- Python 3.6+
- Google API Client Library (`googleapiclient`)
- Pandas (`pandas`)
- OpenPyXL (`openpyxl`)

## How to Use
1. Clone or download this repository.
2. Place the `gsc.py` file in your working directory.
3. Update the following variables in `gsc.py` as needed:
   - `property_uri`: The URL of your Google Search Console property (e.g., `https://www.example.com/`).
   - `start_date`: The start date for the data retrieval (format: `YYYY-MM-DD`).
   - `end_date`: The end date for the data retrieval (format: `YYYY-MM-DD`).
4. Run the script:
   ```bash
   python gsc.py
   ```

## Output
- The script generates two files in the script's directory:
  - `search_analytics_data.xlsx`: A detailed Excel report.
  - `search_analytics_data.csv`: A CSV version of the report.

## Notes
- Ensure you have enabled the Google Search Console API and have the necessary credentials for authentication.
- The script uses `googleapiclient.sample_tools` for authentication.

## License
This project is open-source and available under the MIT License.
