# web_scapper
Scapper for magicbricks.com



This repository contains scripts to collect and scrape rental property data for flats in Pune from [MagicBricks](https://www.magicbricks.com/).


## Overview

The project automates the collection of property URLs and scraping of property details to create a structured dataset for rental flats in Pune. It consists of two main scripts:

1. **`url_collector.py`**  
   - Collects property URLs from MagicBricks Pune rental listings.  
   - Saves URLs to  a text file.

2. **`scraper.py`**  
   - Scrapes details from each property URL, including:  
     - Property ID, Rental Value, Security Deposit  
     - Address, Landmarks, Floor, Area (sqft)  
     - Lift, Furnishing, Flooring, Age of Construction  
     - Property Description  
     - Agent Name & Contact  
   - Handles dynamic content like “View all details” and “Read More”.  
   - Saves the scraped data into a csv required CSV fie

---
How To Use :

1-  Collect all the property listings URL through url_collector.py file .
2- Then Scrape the Property Details form the Scraper.py



## Anti-Scraping & Session Control

- Used **Selenium** with `--disable-blink-features=AutomationControlled` to bypass basic bot detection.  
- Added `time.sleep()` to mimic human browsing behavior and avoid blocking.  
- Try-except blocks ensure missing elements don’t crash the scraper.  
- Sections dynamically expanded to capture all data, achieving ~75% coverage without triggering anti-bot measures.  

---

## Requirements

```bash
pip install selenium pandas beautifulsoup4 requests



