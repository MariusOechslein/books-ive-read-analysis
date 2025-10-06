"""Module for web scraping Google Books URLs."""

import logging
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

from config import BOOKS_URLS_FILE, BOOKS_URLS_RESULTS_FILE, RESULTS_SEPARATOR
from data_loader import read_urls_from_file, write_csv_header, append_csv_row
from google_books_api import get_book_categories_by_isbns

logger = logging.getLogger(__name__)


def scrape_google_books_url(url: str) -> Optional[dict]:
    """
    Scrape book information from a Google Books URL.
    
    Args:
        url: Google Books URL to scrape.
        
    Returns:
        Dictionary containing scraped book information with keys:
        title, author, description, ISBN_list.
        Returns None if scraping fails.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title and author from page title
        title_element = soup.find('head')
        if not title_element:
            logger.error(f"Could not find head element in URL: {url}")
            return None
        
        title_tag = title_element.find('title')
        if not title_tag:
            logger.error(f"Could not find title tag in URL: {url}")
            return None
        
        title_raw = title_tag.text
        title = 'Unknown'
        author = 'Unknown'
        
        # Process title to extract book title and author
        if ' - ' in title_raw:
            parts = title_raw.split(' - ')
            title = parts[0]
            author = parts[1] if len(parts) > 1 else 'Unknown'
        
        logger.info(f"Book Title: {title}")
        logger.info(f"Author: {author}")
        
        # Extract ISBNs from the page
        isbn_list = extract_isbn_from_html(soup)
        
        # Extract description from meta tag
        description = ''
        description_tag = soup.find('meta', attrs={'name': 'description'})
        if description_tag and description_tag.get('content'):
            description = description_tag['content']
            # Replace semicolons to avoid CSV issues
            description = description.replace(';', ',')
        
        logger.info(f"Description: {description[:200]}...")
        
        return {
            'title': title,
            'author': author,
            'description': description,
            'ISBN_list': isbn_list
        }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error scraping URL {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error scraping URL {url}: {e}")
        return None


def extract_isbn_from_html(soup: BeautifulSoup) -> Optional[list[str]]:
    """
    Extract ISBN numbers from parsed HTML.
    
    Looks for ISBN information in the metadata table with id 'metadata_content_table'.
    
    Args:
        soup: BeautifulSoup object containing parsed HTML.
        
    Returns:
        List of ISBN strings, or None if no ISBNs found.
    """
    try:
        table = soup.find('table', attrs={'id': 'metadata_content_table'})
        if not table:
            logger.warning("Could not find metadata_content_table")
            return None
        
        rows = table.find_all('tr', class_='metadata_row')
        for row in rows:
            label = row.find('td', class_='metadata_label')
            if label and 'ISBN' in label.text:
                value = row.find('td', class_='metadata_value')
                if value:
                    isbn = value.text.strip()
                    isbn_list = isbn.split(', ')
                    logger.info(f"Found ISBNs: {isbn_list}")
                    return isbn_list
        
        logger.warning("No ISBN found in metadata table")
        return None
    
    except Exception as e:
        logger.error(f"Error extracting ISBN from HTML: {e}")
        return None


def process_google_books_urls(filename: str = BOOKS_URLS_FILE) -> None:
    """
    Process a list of Google Books URLs and save results to CSV.
    
    Reads URLs from the input file, scrapes each URL, fetches categories
    from the API, and saves all results to BOOKS_URLS_RESULTS_FILE.
    
    Args:
        filename: Path to file containing URLs (one per line).
        
    Raises:
        FileNotFoundError: If the input file doesn't exist.
    """
    try:
        # Read URLs from file
        urls = read_urls_from_file(filename)
        
        # Remove existing results file if it exists
        results_path = Path(BOOKS_URLS_RESULTS_FILE)
        if results_path.exists():
            results_path.unlink()
            logger.info(f"Removed existing results file: {BOOKS_URLS_RESULTS_FILE}")
        
        # Write CSV header
        headers = ['title', 'author', 'description', 'url', 'ISBNs', 'categories']
        write_csv_header(BOOKS_URLS_RESULTS_FILE, headers, RESULTS_SEPARATOR)
        
        # Process each URL
        for url in urls:
            logger.info(f"Scraping URL: {url}")
            print(f"Scraping URL: {url}")
            
            content = scrape_google_books_url(url)
            
            if not content:
                logger.error(f"Failed to scrape URL: {url}")
                print(f"Failed to scrape URL: {url}")
                continue
            
            # Fetch categories using ISBNs
            categories = []
            if content['ISBN_list']:
                categories = get_book_categories_by_isbns(content['ISBN_list'])
            else:
                logger.warning(f"No ISBN found for: {content['title']}")
                print(f"Error ISBN for: {content['title']}")
            
            # Prepare row data
            row_data = {
                'title': content['title'],
                'author': content['author'],
                'description': content['description'],
                'url': url,
                'ISBNs': str(content['ISBN_list']) if content['ISBN_list'] else '',
                'categories': ', '.join(categories) if categories else ''
            }
            
            # Append to CSV
            append_csv_row(BOOKS_URLS_RESULTS_FILE, row_data, headers, RESULTS_SEPARATOR)
            print()
        
        logger.info(f"Completed processing {len(urls)} URLs")
        print(f"Results saved to {BOOKS_URLS_RESULTS_FILE}")
    
    except Exception as e:
        logger.error(f"Error processing Google Books URLs: {e}")
        raise
