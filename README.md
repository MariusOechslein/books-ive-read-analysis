# Books I've Read Analysis

A Python-based tool for analyzing and visualizing personal reading data. This project helps track books you've read, enriches the data using the Google Books API, and creates insightful visualizations.

## Features

- 📚 **Data Loading**: Read and manage book lists from CSV files
- 🔍 **API Integration**: Fetch additional book information from Google Books API
- 🕷️ **Web Scraping**: Extract detailed information from Google Books URLs
- 📊 **Visualizations**: Generate charts showing reading patterns by year, category, and author
- 🗂️ **Modular Design**: Clean, maintainable code structure with separation of concerns

## Project Structure

```
books-ive-read-analysis/
├── main.py                     # Main orchestration script
├── config.py                   # Configuration constants
├── data_loader.py              # CSV file operations
├── google_books_api.py         # Google Books API interactions
├── web_scraper.py              # Web scraping functionality
├── visualization.py            # Plotting and charting
├── books_list.csv              # Input: Your reading list
├── books_urls.csv              # Input: Google Books URLs to scrape
├── books_urls_results.csv      # Output: Scraped results
└── plots/                      # Output: Generated visualizations
```

## Requirements

- Python 3.12+
- pandas
- matplotlib
- requests
- beautifulsoup4

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MariusOechslein/books-ive-read-analysis.git
cd books-ive-read-analysis
```

2. Install dependencies:
```bash
pip install pandas matplotlib requests beautifulsoup4
```

## Usage

### Basic Usage

Run the main script to perform a complete analysis:

```bash
python main.py
```

This will:
1. Load your books list from `books_list.csv`
2. Fetch sample data from Google Books API
3. Scrape sample Google Books URLs
4. Generate visualizations in the `plots/` directory

### Using Individual Modules

You can also import and use individual modules in your own scripts:

```python
from data_loader import read_books
from google_books_api import fetch_book_info
from visualization import plot_books_per_year

# Load books data
books_df = read_books('books_list.csv')

# Fetch book information
book_info = fetch_book_info("The Great Gatsby")

# Create visualizations
plot_books_per_year(books_df)
```

## Input File Format

### books_list.csv

A semicolon-separated file with the following structure:

```
How to win Friends & Influence People;;2019
It's all in your head;Russ;2019
The richest man in babylon;;2020
```

Columns: `title;author;year`

### books_urls.csv

A text file with one Google Books URL per line:

```
https://www.google.com/books/edition/How_to_Win_Friends_and_Influence_People/hCf-DwAAQBAJ?hl=en&gbpv=0
https://www.google.de/books/edition/Der_Steppenwolf/w8k7CgAAQBAJ?hl=de&gbpv=0
```

## Available Functions

### Data Loading (`data_loader.py`)

- `read_books(filename)` - Load books from CSV
- `read_books_extended(filename)` - Load extended books data
- `read_urls_from_file(filename)` - Read URLs from text file
- `write_csv_header(filename, headers)` - Write CSV header
- `append_csv_row(filename, data, columns)` - Append row to CSV

### Google Books API (`google_books_api.py`)

- `fetch_book_info(query)` - Fetch book information by title/author
- `get_book_categories_by_isbns(isbn_list)` - Get categories for ISBN list
- `extend_books_with_api(books_pd)` - Extend DataFrame with API data

### Web Scraping (`web_scraper.py`)

- `scrape_google_books_url(url)` - Scrape a single Google Books URL
- `extract_isbn_from_html(soup)` - Extract ISBN from parsed HTML
- `process_google_books_urls(filename)` - Process multiple URLs from file

### Visualization (`visualization.py`)

- `plot_books_per_year(books_pd)` - Bar chart of books per year
- `plot_books_per_column(books_extended_pd, column)` - Chart by category/author
- `plot_books_per_column_per_year(...)` - Multi-year comparison charts

## Configuration

All configuration constants can be found in `config.py`:

- File paths and names
- CSV separators
- API endpoints
- Visualization settings
- Analysis year ranges

## Logging

The application creates a log file (`books_analysis.log`) with detailed information about:
- Data loading operations
- API requests and responses
- Scraping activities
- Errors and warnings

Log format:
```
2025-10-06 15:25:01,396 - __main__ - INFO - Loading books data...
2025-10-06 15:25:01,398 - data_loader - INFO - Successfully loaded 69 books
```

## Error Handling

The refactored code includes comprehensive error handling:
- File not found errors
- Network request failures
- Invalid CSV formats
- Missing data fields
- API rate limiting

All errors are logged and handled gracefully without crashing the application.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Future Enhancements

Possible improvements for future versions:
- [ ] Add unit tests
- [ ] Support for multiple data sources
- [ ] Interactive web dashboard
- [ ] Export reports to PDF
- [ ] Integration with Goodreads API
- [ ] Reading statistics and insights

## License

This project is open source and available for personal use.

## Author

Marius Oechslein

## Acknowledgments

- Google Books API for providing book data
- BeautifulSoup for HTML parsing capabilities
- Pandas and Matplotlib for data analysis and visualization