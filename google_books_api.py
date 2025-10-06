"""Module for interacting with the Google Books API."""

import logging
from typing import Optional

import pandas as pd
import requests

from config import GOOGLE_BOOKS_API_URL

logger = logging.getLogger(__name__)


def fetch_book_info(query: str) -> Optional[dict]:
    """
    Fetch book information from Google Books API.
    
    Args:
        query: Search query string (book title, author, ISBN, etc.).
        
    Returns:
        Dictionary containing book information or None if not found.
        Keys include: title, authors, publishedDate, pageCount, categories,
        averageRating, ratingsCount, thumbnail.
    """
    try:
        url = f"{GOOGLE_BOOKS_API_URL}?q={query}"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            logger.warning(f"API returned status code {response.status_code} for query: {query}")
            return None
        
        data = response.json()
        
        if 'items' not in data or not data['items']:
            logger.info(f"No books found for query: {query}")
            return None
        
        book_info = data['items'][0]['volumeInfo']
        result = {
            'title': book_info.get('title', 'N/A'),
            'authors': book_info.get('authors', ['N/A']),
            'publishedDate': book_info.get('publishedDate', 'N/A'),
            'pageCount': book_info.get('pageCount', 'N/A'),
            'categories': book_info.get('categories', ['N/A']),
            'averageRating': book_info.get('averageRating', 'N/A'),
            'ratingsCount': book_info.get('ratingsCount', 'N/A'),
            'thumbnail': book_info.get('imageLinks', {}).get('thumbnail', 'N/A')
        }
        
        logger.info(f"Successfully fetched info for: {result['title']}")
        return result
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error fetching book info for query '{query}': {e}")
        return None
    except Exception as e:
        logger.error(f"Error fetching book info for query '{query}': {e}")
        return None


def get_book_categories_by_isbns(isbn_list: list[str]) -> list[str]:
    """
    Fetch book categories from Google Books API using ISBN numbers.
    
    Args:
        isbn_list: List of ISBN numbers.
        
    Returns:
        List of unique categories found across all ISBNs.
    """
    categories = []
    
    for isbn in isbn_list:
        try:
            url = f"{GOOGLE_BOOKS_API_URL}?q=isbn:{isbn}"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                logger.warning(f"Failed to fetch data for ISBN: {isbn}")
                continue
            
            data = response.json()
            
            if "items" not in data or not data["items"]:
                logger.info(f"No books found for ISBN: {isbn}")
                continue
            
            # Extract categories from all items
            for item in data["items"]:
                volume_info = item.get("volumeInfo", {})
                item_categories = volume_info.get("categories", [])
                categories.extend(item_categories)
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching categories for ISBN {isbn}: {e}")
            continue
        except Exception as e:
            logger.error(f"Error fetching categories for ISBN {isbn}: {e}")
            continue
    
    # Remove duplicates and return
    unique_categories = list(set(categories))
    logger.info(f"Found {len(unique_categories)} unique categories for {len(isbn_list)} ISBNs")
    return unique_categories


def extend_books_with_api(books_pd: pd.DataFrame) -> pd.DataFrame:
    """
    Extend books DataFrame with information from Google Books API.
    
    This function queries the API for each book and asks for user confirmation
    before adding the retrieved information.
    
    Args:
        books_pd: DataFrame containing books with at least 'title' and 'author' columns.
        
    Returns:
        Extended DataFrame with additional columns from API data.
    """
    extended_data = []
    
    for _, row in books_pd.iterrows():
        query = row['title']
        if pd.notna(row.get('author')):
            query += f" {row['author']}"
        
        logger.info(f"Fetching data for: {query}")
        print(f"Fetching data for: {query}")
        
        book_info = fetch_book_info(query)
        
        if book_info:
            print("Book found:")
            for key, value in book_info.items():
                print(f"  {key}: {value}")
            
            user_input = input("Is this information correct? (y/n): ")
            
            if user_input.lower() == 'y':
                extended_data.append({
                    **row,
                    'found_title': book_info['title'],
                    'found_author': book_info['authors'],
                })
            else:
                print("Book information rejected by user.")
                extended_data.append({
                    **row,
                    'found_title': 'Not Found',
                    'found_author': 'Not Found',
                })
        else:
            logger.warning(f"Error fetching data for: {row['title']}")
            print(f"Error fetching data for: {row['title']}")
            extended_data.append(row)
    
    return pd.DataFrame(extended_data)
