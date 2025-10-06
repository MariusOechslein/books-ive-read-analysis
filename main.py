"""
Main script for analyzing books read.

This script orchestrates the analysis of books data including:
- Loading books from CSV files
- Fetching additional information from Google Books API
- Scraping Google Books URLs for detailed information
- Creating visualizations of books read per year, category, and author
"""

import logging
import sys

import pandas as pd

from data_loader import read_books
from google_books_api import fetch_book_info
from web_scraper import scrape_google_books_url, process_google_books_urls
from visualization import plot_books_per_column, plot_books_per_column_per_year

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('books_analysis.log')
    ]
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point for the books analysis script."""
    try:
        # Load books data
        logger.info("Loading books data...")
        books_pd = read_books()
        print(books_pd.tail())
        print()

        # Uncomment to load extended books data
        # books_extended_pd = read_books_extended()
        # print(books_extended_pd.tail())
        # print()

        # Fetch book info from Google Books API
        print("Fetch book info from google books api")
        book_details = fetch_book_info("How to win Friends & Influence People")
        print(book_details)
        print()

        # Scrape book URLs
        print("Scrape book url")
        scrape_google_books_url(
            "https://www.google.com/books/edition/How_to_Win_Friends_and_Influence_People/hCf-DwAAQBAJ?hl=en&gbpv=0"
        )
        scrape_google_books_url(
            "https://www.google.de/books/edition/Der_Steppenwolf/w8k7CgAAQBAJ?hl=de&gbpv=0"
        )
        print()

        # Process Google Books URLs (this takes a long time, so it's commented out)
        print("Get info from google books urls")
        # process_google_books_urls(filename="books_urls.csv")
        print()

        # Uncomment to plot books per year
        # plot_books_per_year(books_pd)

        # Create visualizations
        print("Plot books per category...")
        books_extended_pd = pd.read_csv('books_urls_results.csv', sep=';')
        plot_books_per_column(books_extended_pd, column='categories')

        print("Plot books per author...")
        plot_books_per_column(books_extended_pd, column='author')

        # Create plots per year
        plot_books_per_column_per_year(books_extended_pd, books_pd, column='categories')

        logger.info("Analysis completed successfully")
        print("\nAnalysis completed successfully!")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
