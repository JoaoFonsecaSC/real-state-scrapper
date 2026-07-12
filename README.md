🏠 VivaReal Rent Scraper

This project is a Python based web scraper designed to collect rental apartment data from VivaReal listings, focusing on properties located in the Greater Florianópolis region, Santa Catarina.

The goal of this project is to practice real world web scraping techniques, including pagination handling, data extraction from listing cards, and data normalization for analysis, and to persist the results to a cloud data lake using PySpark.

📌 Project Overview

The scraper navigates through the rental listing pages of each configured city and extracts structured information from every property card available in the search results.

The collected data is written to Google Cloud Storage as a Parquet file, simulating a small scale data collection pipeline for exploratory analysis and educational purposes.

🌎 Cities Collected

The scraper currently collects apartment rentals from the following cities in Santa Catarina:

- São José
- Palhoça
- Florianópolis

Cities are defined in the `CITIES` list in `main.py` — the search URL for each one is built dynamically by `build_url()`, so adding a new city is just a matter of appending a new entry (display name, name without accents, URL slug, latitude, longitude).

📊 Data Collected

For each rental listing, the scraper extracts the following fields:

- City — city the listing was collected from.
- Title — neighborhood / location headline of the listing.
- Area — property size in square meters.
- Beds — number of bedrooms.
- Address — street or address information when present.
- Price — monthly rent value.
- Condo — condominium fee (0 when not informed).
- IPTU — property tax (0 when not informed).
- Link — direct link to the individual property page.

🛠️ Tech Stack

- Python 3.x
- Selenium — drives a headless-capable Chrome session to load and paginate the listings.
- webdriver-manager — resolves and installs the matching ChromeDriver automatically.
- PySpark — builds the DataFrame and writes it out as Parquet.
- GCS Connector (Hadoop) — lets Spark write directly to Google Cloud Storage.

⚙️ Requirements

- Java 17 — required by Spark. The path is set in `main.py` via `JAVA_HOME` (`/usr/lib/jvm/java-17-openjdk-amd64`); adjust it if your installation differs.
- A GCP service account key named `chave-gcp.json`, placed next to `main.py`. This file is git-ignored and must never be committed.
- The service account needs the `Storage Object Admin` (`roles/storage.objectAdmin`) role on the destination bucket.

🚀 How to Run

1. Clone the repository
```
git clone https://github.com/seu-usuario/vivareal-rent-scraper.git
cd vivareal-rent-scraper
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Add your GCP credentials
Place your service account key as `chave-gcp.json` in the same directory as `main.py`.

4. Run the scraper
```
python main.py
```

After execution, the extracted rental listings are written as a Parquet file to the configured GCS bucket (`gs://rent_scrapper/raw/rents_info.parquet`).
