#!/usr/bin/env python3
"""
Pastebin Keyword Crawler

This script scrapes Pastebin's public archive for pastes containing crypto-related 
keywords or Telegram links and saves the results to a JSONL file.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
import random
import re
import logging
from concurrent.futures import ThreadPoolExecutor
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("crawler.log"),
        logging.StreamHandler()
    ]
)

class PastebinCrawler:
    """Crawler for Pastebin that searches for crypto and Telegram-related content."""
    
    def __init__(self, keywords=None, output_file="keyword_matches.jsonl"):
        """Initialize the crawler with keywords to search for."""
        self.archive_url = "https://pastebin.com/archive"
        self.raw_paste_url = "https://pastebin.com/raw/{}"
        
        # Default keywords if none are provided
        self.keywords = keywords or [
            "crypto", "bitcoin", "ethereum", "blockchain", "t.me", 
            "btc", "eth", "nft", "defi", "wallet", "binance", "coinbase"
        ]
        
        self.output_file = output_file
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def get_archive_paste_ids(self):
        """Fetch and extract the latest 30 paste IDs from the archive page."""
        try:
            response = requests.get(self.archive_url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
     
            paste_links = soup.select('table.maintable tr td:nth-child(1) a')
            
          
            paste_ids = []
            for link in paste_links:
                href = link.get('href')
                if href and href.startswith('/'):
                    paste_id = href.lstrip('/')
                    paste_ids.append(paste_id)
            
            logging.info(f"Found {len(paste_ids)} paste IDs in the archive")
            return paste_ids
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching archive page: {e}")
            return []

    def fetch_paste_content(self, paste_id):
        """Fetch the content of a paste given its ID."""
        url = self.raw_paste_url.format(paste_id)
        
        try:
          
            time.sleep(random.uniform(1.0, 3.0))
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching paste {paste_id}: {e}")
            return None

    def check_keywords(self, content):
        """Check if any keywords are present in the content."""
        if not content:
            return []
        
        # Convert content to lowercase for case-insensitive matching
        content_lower = content.lower()
        
        # Find all keywords that are present in the content
        found_keywords = []
        for keyword in self.keywords:
            # Use word boundary for more accurate matching
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, content_lower) or keyword.lower() in content_lower:
                found_keywords.append(keyword)
                
        return found_keywords

    def process_paste(self, paste_id):
        """Process a single paste: fetch content, check keywords, save if matched."""
        logging.info(f"Processing paste: {paste_id}")
        
        content = self.fetch_paste_content(paste_id)
        if not content:
            logging.warning(f"Could not fetch content for paste {paste_id}")
            return None
        
        keywords_found = self.check_keywords(content)
        
        if keywords_found:
            logging.info(f"Found keywords {keywords_found} in paste {paste_id}")
            
            # Create result object
            now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            result = {
                "source": "pastebin",
                "context": f"Found crypto-related content in Pastebin paste ID {paste_id}",
                "paste_id": paste_id,
                "url": self.raw_paste_url.format(paste_id),
                "discovered_at": now,
                "keywords_found": keywords_found,
                "status": "pending"
            }
            
            return result
        else:
            logging.info(f"No keywords found in paste {paste_id}")
            return None

    def save_result(self, result):
        """Save a single result to the output file."""
        if not result:
            return
            
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result) + '\n')
            
    def run(self, max_workers=5):
        """Run the crawler to process all pastes from the archive."""
        logging.info("Starting Pastebin crawler")
        
        # Get paste IDs from archive
        paste_ids = self.get_archive_paste_ids()
        if not paste_ids:
            logging.error("No paste IDs found. Exiting.")
            return
        
        # Clear the output file if it exists
        open(self.output_file, 'w').close()
        
        # Use multi-threading to process pastes faster
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.process_paste, paste_ids))
            
       
        for result in results:
            if result:
                self.save_result(result)
                

        match_count = sum(1 for r in results if r)
        logging.info(f"Crawler finished. Found {match_count} pastes with matching keywords.")


if __name__ == "__main__":
    
    crawler = PastebinCrawler()
    crawler.run()