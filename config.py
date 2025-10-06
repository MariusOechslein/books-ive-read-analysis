"""Configuration constants for the books analysis project."""

from pathlib import Path
from typing import Final

# File paths
BOOKS_LIST_FILE: Final[str] = "books_list.csv"
BOOKS_EXTENDED_FILE: Final[str] = "books_extended.csv"
BOOKS_URLS_FILE: Final[str] = "books_urls.csv"
BOOKS_URLS_RESULTS_FILE: Final[str] = "books_urls_results.csv"
PLOTS_DIR: Final[Path] = Path("plots")

# CSV separators
BOOKS_LIST_SEPARATOR: Final[str] = ';'
BOOKS_EXTENDED_SEPARATOR: Final[str] = ','
RESULTS_SEPARATOR: Final[str] = ';'

# API endpoints
GOOGLE_BOOKS_API_URL: Final[str] = "https://www.googleapis.com/books/v1/volumes"

# Visualization settings
FIGURE_SIZE_LARGE: Final[tuple[int, int]] = (20, 15)
FIGURE_SIZE_MEDIUM: Final[tuple[int, int]] = (12, 6)
ROTATION_ANGLE: Final[int] = 45

# Years for analysis
ANALYSIS_YEARS: Final[list[int]] = [2019, 2020, 2021, 2022, 2023, 2024, 2025]

# Column names
COLUMN_TITLE: Final[str] = 'title'
COLUMN_AUTHOR: Final[str] = 'author'
COLUMN_YEAR: Final[str] = 'year'
COLUMN_CATEGORIES: Final[str] = 'categories'
COLUMN_DESCRIPTION: Final[str] = 'description'
