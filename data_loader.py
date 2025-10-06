"""Module for loading and processing CSV data files."""

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

from config import (
    BOOKS_LIST_FILE,
    BOOKS_EXTENDED_FILE,
    BOOKS_LIST_SEPARATOR,
    BOOKS_EXTENDED_SEPARATOR,
    COLUMN_TITLE,
    COLUMN_AUTHOR,
    COLUMN_YEAR,
)

logger = logging.getLogger(__name__)


def read_books(filename: str = BOOKS_LIST_FILE) -> pd.DataFrame:
    """
    Read books list from CSV file.
    
    Args:
        filename: Path to the CSV file containing books list.
        
    Returns:
        DataFrame containing books data with columns: title, author, year.
        
    Raises:
        FileNotFoundError: If the file doesn't exist.
        pd.errors.ParserError: If the file format is invalid.
    """
    try:
        filepath = Path(filename)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filename}")
        
        books_pd = pd.read_csv(
            filename,
            sep=BOOKS_LIST_SEPARATOR,
            names=[COLUMN_TITLE, COLUMN_AUTHOR, COLUMN_YEAR]
        )
        logger.info(f"Successfully loaded {len(books_pd)} books from {filename}")
        return books_pd
    except Exception as e:
        logger.error(f"Error reading books from {filename}: {e}")
        raise


def read_books_extended(filename: str = BOOKS_EXTENDED_FILE) -> pd.DataFrame:
    """
    Read extended books data from CSV file.
    
    Args:
        filename: Path to the CSV file containing extended books data.
        
    Returns:
        DataFrame containing extended books data.
        
    Raises:
        FileNotFoundError: If the file doesn't exist.
        pd.errors.ParserError: If the file format is invalid.
    """
    try:
        filepath = Path(filename)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filename}")
        
        books_pd = pd.read_csv(filename, sep=BOOKS_EXTENDED_SEPARATOR)
        logger.info(f"Successfully loaded {len(books_pd)} extended books from {filename}")
        return books_pd
    except Exception as e:
        logger.error(f"Error reading extended books from {filename}: {e}")
        raise


def read_urls_from_file(filename: str) -> list[str]:
    """
    Read URLs from a text file, one URL per line.
    
    Args:
        filename: Path to the file containing URLs.
        
    Returns:
        List of URL strings, with empty lines filtered out.
        
    Raises:
        FileNotFoundError: If the file doesn't exist.
    """
    try:
        filepath = Path(filename)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filename}")
        
        with open(filename, "r", encoding='utf-8') as f:
            urls = [url.strip() for url in f.readlines() if url.strip()]
        
        logger.info(f"Successfully loaded {len(urls)} URLs from {filename}")
        return urls
    except Exception as e:
        logger.error(f"Error reading URLs from {filename}: {e}")
        raise


def write_csv_header(filename: str, headers: list[str], separator: str = ';') -> None:
    """
    Write CSV header to a file.
    
    Args:
        filename: Path to the output file.
        headers: List of column header names.
        separator: Column separator character.
    """
    try:
        with open(filename, "w", encoding='utf-8') as f:
            f.write(separator.join(headers) + "\n")
        logger.info(f"Written header to {filename}")
    except Exception as e:
        logger.error(f"Error writing header to {filename}: {e}")
        raise


def append_csv_row(filename: str, data: dict, columns: list[str], separator: str = ';') -> None:
    """
    Append a row to a CSV file.
    
    Args:
        filename: Path to the output file.
        data: Dictionary containing row data.
        columns: List of column names in the order they should appear.
        separator: Column separator character.
    """
    try:
        with open(filename, "a", encoding='utf-8') as f:
            row_values = [str(data.get(col, '')) for col in columns]
            f.write(separator.join(row_values) + "\n")
    except Exception as e:
        logger.error(f"Error appending row to {filename}: {e}")
        raise
