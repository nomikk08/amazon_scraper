import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent

# PROXIES = [
# #     'http://91.134.148.198:8081',
# #     'http://149.56.106.104:3128',
# #     'http://161.97.79.165:3128',
# #     'http://103.10.82.86:3128',
# #     'http://195.123.212.199:3128',
# #     'http://200.105.215.22:33630',
# #     'http://51.222.146.133:3128',
# #     'http://62.33.207.202:3128',
# #     'http://91.234.127.222:53281',
# #     'http://88.198.24.108:8080',
# # ]

# # # Function to get random proxy
# # def get_random_proxy():
# #     return random.choice(PROXIES)

def get_headers():
    """
    Generates a header with a random User-Agent to mimic different browsers.
    Returns:
        headers (dict): A dictionary with randomized User-Agent and language preferences.
    """
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,  # Get a random User-Agent
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'DNT': '1'  # Do not track request
    }
    return headers

# Function to parse product details from a page
def parse_product(product):
    """
    Extracts product information (name, brand, ASIN, SKU, and image URL) from a product listing on Amazon.
    
    Args:
        product (BeautifulSoup object): A single product block from the Amazon search page.
    
    Returns:
        dict: A dictionary containing the product's name, brand, ASIN, SKU, and image URL.
    """
    # Product name
    name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
    name = name.text if name else 'N/A'
    
    # Amazon-specific tags to find ASIN and brand
    asin = product['data-asin'] if 'data-asin' in product.attrs else 'N/A'
    
    # Sometimes SKU is not available, so use default value
    sku = product.find('span', {'class': 'a-size-small a-color-base'}) 
    sku = sku.text if sku else 'N/A'
    
    brand = product.find('span', {'class': 'a-size-medium a-color-base'})
    brand = brand.text if brand else 'N/A'

    # Image URL of the product
    image_tag = product.find('img', {'class': 's-image'})
    image_url = image_tag['src'] if image_tag else 'N/A'

    return {
        'name': name,
        'brand': brand,
        'ASIN': asin,
        'SKU': sku,
        'image_url': image_url,
    }

# Function to scrape products from a specific page
def scrape_page(brand, url):
    """
    Scrapes a single Amazon search results page for products of a specific brand.
    
    Args:
        brand (str): The name of the brand to filter products.
        url (str): The URL of the Amazon search page.
    
    Returns:
        tuple: A tuple containing:
            - products (list): A list of dictionaries with the details of each product.
            - soup (BeautifulSoup object): Parsed HTML of the page, used to extract pagination details.
    """
    products = []
    try:
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            if 'captcha' in response.text.lower():
                print(f"CAPTCHA encountered on attempt {i+1}")
                time.sleep(60)  # Wait before retrying
            else:
                soup = BeautifulSoup(response.text, 'html.parser')
                product_list = soup.find_all('div', {'data-component-type': 's-search-result'})

            for product in product_list:
                product_details = parse_product(product)
                if brand.lower() in product_details['brand'].lower():
                    products.append(product_details)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    return products, soup

# Function to get the total number of pages from the first page
def get_total_pages(soup):
    """
    Extracts the total number of pages from the pagination element on the search results page.
    
    Args:
        soup (BeautifulSoup object): Parsed HTML of the Amazon search results page.
    
    Returns:
        total_pages (int): The total number of pages available for the search results. Defaults to 5 if not found.
    """
    page = soup.find('span', {'class': 's-pagination-item s-pagination-disabled'})
    total_pages = int(page.text) if page else 5  # Default to 5 if not found
    return total_pages

def scrape_amazon(brand):
    """
    Scrapes all product listings for a specific brand across multiple pages of Amazon search results.
    
    Args:
        brand (str): The brand name to search for.
    
    Returns:
        all_products (list): A list of dictionaries containing product details scraped from all pages.
    """
    all_products = []  # List to store all scraped products
    
    # Initial search URL based on the brand
    base_url = f"https://www.amazon.com/s?k={brand}"
    
    # Scrape the first page to determine the total number of pages
    first_page_products, first_soup = scrape_page(brand, base_url)
    all_products.extend(first_page_products)  # Add products from the first page to the list
    
    # Determine total number of pages from the first page
    total_pages = get_total_pages(first_soup)
    print(f"Total pages found: {total_pages}")

    # Loop through the rest of the pages (starting from page 2)
    for page_num in range(2, total_pages + 1):
        url = f"{base_url}&page={page_num}"  # Construct the URL for each page
        print(f"Scraping page {page_num} of {total_pages}: {url}")
        
        # Scrape the current page
        products, _ = scrape_page(brand, url)
        all_products.extend(products)  # Add the products to the overall list

        # Introduce a random delay between requests to avoid detection
        time.sleep(random.uniform(2, 6))

        # Stop if no products are found (this could indicate an error or end of results)
        if not products:
            print(f"No products found on page {page_num}, stopping...")
            break

    return all_products