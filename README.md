🏠 VivaReal Rent Scraper

This project is a Python based web scraper designed to collect rental apartment data from VivaReal listings, focusing on properties located in São José, Santa Catarina.

The goal of this project is to practice real world web scraping techniques, including pagination handling, data extraction from listing cards, and data normalization for analysis.

📌 Project Overview

The scraper navigates through rental listing pages and extracts structured information from each property card available in the search results.

The collected data is intended for exploratory analysis and educational purposes, simulating a small scale data collection pipeline.

📊 Data Collected

For each rental listing, the scraper extracts the following fields:

Title
Short description or headline of the listing.

Price
Monthly rent value, cleaned and converted to float.

Bedrooms
Number of bedrooms available.

Bathrooms
Number of bathrooms, when available.

Parking Spaces
Number of parking spots.

Area
Property size in square meters.

Location
Neighborhood or address information when present.

Listing URL
Direct link to the individual property page.

All extracted data is exported to a CSV file for further analysis.

🛠️ Tech Stack

Python 3.x

Requests
Handles HTTP requests and page retrieval.

Selenium
Parses HTML content and extracts structured data.

Pandas
Cleans, normalizes, and exports data to CSV.



🚀 How to Run
1. Clone the repository
git clone https://github.com/seu-usuario/vivareal-rent-scraper.git
cd vivareal-rent-scraper

2. Install dependencies
pip install -r requirements.txt

3. Run the scraper
python main.py


After execution, a CSV file containing the extracted rental listings will be generated in the project root directory.