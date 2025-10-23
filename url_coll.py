#!/usr/bin/env python3
"""
URL Collection script for Pune rental properties
"""

import requests
from bs4 import BeautifulSoup
import time
import random

def collect_property_urls():
    """
    Collect property URLs from MagicBricks
    """
    print("Collecting property URLs from MagicBricks...")
    
    base_url = "https://www.magicbricks.com/property-for-rent-in-pune-pppfr"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    urls = []
    
    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find property links
            property_links = soup.find_all('a', href=True)
            
            for link in property_links:
                href = link.get('href')
                if href and 'propertyDetails' in href:
                    if href.startswith('/'):
                        href = 'https://www.magicbricks.com' + href
                    urls.append(href)
            
            print(f"Collected {len(urls)} URLs")
            
            # Save URLs
            with open('prop_urls.txt', 'w') as f:
                for url in urls:
                    f.write(url + '\n')
            
            print("URLs saved to prop_urls.txt")
            
        else:
            print(f"Failed to fetch page: {response.status_code}")
            
    except Exception as e:
        print(f"Error collecting URLs: {e}")
    
    return urls

if __name__ == "__main__":
    urls = collect_property_urls()
