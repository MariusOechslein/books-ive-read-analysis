import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

def read_books(filename="books_list.csv"):
    books_pd = pd.read_csv(filename, sep=';', names=['title', 'author', 'year'])
    return books_pd

def read_books_extended(filename="books_extended.csv"):
    books_pd = pd.read_csv(filename, sep=',')
    return books_pd

def plot_books_per_year(books_pd):
    # Visualization books per year
    # TODO: Add Notes to plot that bachelor 2019 - 2022, master 2023 - 2025, start of work 2025
    books_per_year = books_pd['year'].value_counts().sort_index()
    plt.figure(figsize=(12, 6))
    plt.bar(books_per_year.index, books_per_year.values)
    plt.xlabel('Year')
    plt.ylabel('Number of Books')
    plt.title('Books Read Per Year')
    plt.xticks(rotation=45)
    plt.savefig('plots/books_per_year.png')

# Call google books api to get more information about the books
def fetch_book_info(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            book_info = data['items'][0]['volumeInfo']
            return {
                'title': book_info.get('title', 'N/A'),
                'authors': book_info.get('authors', ['N/A']),
                'publishedDate': book_info.get('publishedDate', 'N/A'),
                'pageCount': book_info.get('pageCount', 'N/A'),
                'categories': book_info.get('categories', ['N/A']),
                'averageRating': book_info.get('averageRating', 'N/A'),
                'ratingsCount': book_info.get('ratingsCount', 'N/A'),
                'thumbnail': book_info.get('imageLinks', {}).get('thumbnail', 'N/A')
            }
    return None

def extend_books_with_api(books_pd) -> pd.DataFrame:
    extended_data = []
    for _, row in books_pd.iterrows():
        query = row['title']
        if pd.notna(row['author']):
            query += f" {row['author']}"
        print(f"Fetching data for: {query}")
        book_info = fetch_book_info(query)
        # Show result with title, authors, publishedDate and let user decide if it's correct with y or n. If n, save "not found" in the row
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
                print("Book information not found.")
                extended_data.append({
                    **row,
                    'found_title': 'Not Found',
                    'found_author': 'Not Found',
                })
        else:
            print("Error fetching data for:", row['title'])
            extended_data.append(row)
    return pd.DataFrame(extended_data)

def plot_books_per_column(books_extended_pd, column='categories', save_file_name_suffix=''):
    # Plot num of books per categories box plot
    categories_series = books_extended_pd[column].dropna().apply(lambda x: x.split(', '))
    all_categories = [category for sublist in categories_series for category in sublist]
    categories_count = pd.Series(all_categories).value_counts()
    plt.figure(figsize=(20, 15))
    categories_count.plot(kind='bar')
    plt.xlabel(column.capitalize())
    plt.ylabel('Number of Books')
    plt.title('Books per ' + column.capitalize())
    plt.xticks(rotation=45, ha='right')
    plt.savefig('plots/books_per_' + column + save_file_name_suffix + '.png')
    plt.close()

def scrape_google_books_url(url):
    response = requests.get(url)
    # Extract info from <head><title>
    soup = BeautifulSoup(response.text, 'html.parser')
    title_raw = soup.find('head').find('title').text
    # Process title to get title and author
    if ' - ' in title_raw:
        title = title_raw.split(' - ')[0]
        author = title_raw.split(' - ')[1] if len(title_raw.split(' - ')) > 1 else 'Unknown'
    print("Book Title:", title)
    print("Author:", author)

    # Extract ISBNs from the page
    isbn_list = extract_isbn_from_html(soup)

    # Save full html to file
    #with open("scraped_page.html", "w", encoding='utf-8') as f:
    #   f.write(response.text)

    # Extract info from <meta name="description"> content
    description = soup.find('meta', attrs={'name': 'description'})['content']
    print("Description:", description[:200], "...")
    return {
        'title': title,
        'author': author,
        'description': description.replace(';', ','),
        'ISBN_list': isbn_list
    }

def extract_isbn_from_html(soup):
    """
    From HTML page:
    #<table id="metadata_content_table">
        #<tr class="metadata_row">
            #<td class="metadata_label"><span dir=ltr>ISBN</span></td>
            #<td class="metadata_value">
    """
    table = soup.find('table', attrs={'id': 'metadata_content_table'})
    if not table:
        return None
    rows = table.find_all('tr', class_='metadata_row')
    for row in rows:
        label = row.find('td', class_='metadata_label')
        if label and 'ISBN' in label.text:
            value = row.find('td', class_='metadata_value')
            if value:
                isbn = value.text.strip()
                return isbn.split(', ') # Return list of ISBNs
    return None

def process_google_books_urls(filename="books_urls.csv"):
    # Open books_urls.csv and read line by line
    with open(filename, "r") as f:
        urls = f.readlines()

    import os
    if os.path.exists("books_urls_results.csv"):
        os.remove("books_urls_results.csv")
    with open("books_urls_results.csv", "w", encoding='utf-8') as f:
        f.write("title;author;description;url;ISBNs;categories\n")

    for url in urls:
        url = url.strip()
        if url:
            print(f"Scraping URL: {url}")
            content = scrape_google_books_url(url)
            categories = get_book_categories_by_isbns(content['ISBN_list']) if content['ISBN_list'] else print("Error ISBN for:", content['title'])
            
            # Append results to books_urls_results.csv
            with open("books_urls_results.csv", "a", encoding='utf-8') as f:
                f.write(f"{content['title']};{content['author']};{content['description']};{url};{content['ISBN_list']};{categories}\n")
            print()

def get_book_categories_by_isbns(isbn_list):
    categories = []
    for isbn in isbn_list:
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to fetch data")
            continue

        data = response.json()
        if "items" not in data or not data["items"]:
            print("No books found for this ISBN")
            continue

        # Take the first book item, extract categories if present
        # Don't only take first category, take all categories
        for item in data["items"]:
            volume_info = item.get("volumeInfo", {})
            categories.extend(volume_info.get("categories", []))
    # Drop duplicates
    categories = list(set(categories))
    return categories

def plot_books_per_column_per_year(books_extended_pd, books_pd, column='categories'):
    # Add year column to books_extended_pd based on the original books_pd line for line if pd length is the same
    if len(books_extended_pd) == len(books_pd):
        books_extended_pd['year'] = books_pd['year']
    else:
        print("Error: Length of books_extended_pd and books_pd do not match")
        exit(1)

    # Analysis per year 2023
    for year in [2019, 2020, 2021, 2022, 2023, 2024, 2025]:
        books_year = books_extended_pd[books_extended_pd['year'] == year]
        plot_books_per_column(books_year, column='categories', save_file_name_suffix=f"_{year}")
    # Make one big plot with all 7 years as subplots.
    plt.figure(figsize=(20, 15))
    for i, year in enumerate([2019, 2020, 2021, 2022, 2023, 2024, 2025]):
        plt.subplot(3, 3, i+1)
        books_year = books_extended_pd[books_extended_pd['year'] == year]
        categories_series = books_year['categories'].dropna().apply(lambda x: x.split(', '))
        all_categories = [category for sublist in categories_series for category in sublist]
        categories_count = pd.Series(all_categories).value_counts()
        categories_count.plot(kind='bar')
        plt.xlabel('Categories')
        plt.ylabel('Number of Books')
        plt.title(f'Books per Categories in {year}')
        plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('plots/books_per_categories_per_year.png')
    plt.close()

if __name__ == "__main__":
    books_pd = read_books()
    print(books_pd.tail())
    print()

    #books_extended_pd = read_books_extended()
    #print(books_extended_pd.tail())
    #print()

    print("Fetch book info from google books api")
    book_details = fetch_book_info("How to win Friends & Influence People")#("Der grosse Sommer")
    print(book_details)
    print()

    print("Scrape book url")
    scrape_google_books_url("https://www.google.com/books/edition/How_to_Win_Friends_and_Influence_People/hCf-DwAAQBAJ?hl=en&gbpv=0")
    scrape_google_books_url("https://www.google.de/books/edition/Der_Steppenwolf/w8k7CgAAQBAJ?hl=de&gbpv=0")
    print()

    # Takes long
    print("Get info from google books urls")
    #process_google_books_urls(filename="books_urls.csv")
    print()

    # plot_books_per_year(books_pd)


    print("Plot books per category...")
    books_extended_pd = pd.read_csv('books_urls_results.csv', sep=';')
    plot_books_per_column(books_extended_pd, column='categories')

    print("Plot books per author...")
    plot_books_per_column(books_extended_pd, column='author')

    plot_books_per_column_per_year(books_extended_pd, books_pd, column='categories')
