import sys
import requests
import re
import time
import json
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin
from tqdm import tqdm
from rich import print
from rich.table import Table
from rich.console import Console
from datetime import datetime
from getpass import getpass
import urllib.robotparser
import textwrap
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


# ============================================================
# DEVELOPER LOG
# Last Changed: January 17
# What Changed: Code organization, code cleanup
# Changed by: Owen Orcan
# ============================================================

# ============================================================
# UTILITY FUNCTIONS
# General-purpose functions used across the script.
# ============================================================

def extract_domain(url):
    """
    Extracts the domain from a given URL.
    Parameters:
    url (str): The URL from which to extract the domain.
    Returns:
    str: Extracted domain or None if not found.
    """
    pattern = r"https?://([A-Za-z0-9.-]+)"
    match = re.search(pattern, url)
    return match.group(0) if match else None

def is_allowed_by_robots_txt(url):
    """
    Checks if the given URL is allowed to be crawled according to the robots.txt file.
    Parameters:
    url (str): The URL to be checked.
    Returns:
    bool: True if crawling is allowed, False otherwise.
    """
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url + "/robots.txt")
    rp.read()
    return rp.can_fetch("*", url)

def dynamic_delay(response):
    """
    Dynamically delays the next request based on the server's response.
    Parameters:
    response (Response): The response object from the previous request.
    Returns:
    None
    """
    try:
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 10))
            print("YiraBot: Website Server Is Overwhelmed, Waiting Before Starting Crawl.")
            time.sleep(retry_after)
        else:
            print("YiraBot: Starting Crawl.")
            time.sleep(1)  # Default delay for non-429 responses
    except KeyboardInterrupt or EOFError:
        sys.exit("YiraBot: Crawl Aborted")

def login_successful(response, expected_response):
    """
    Determines if the login was successful by checking for redirection to a specific URL.
    Parameters:
    response (Response): The response object from the login request.
    expected_response (str): The expected URL after a successful login.
    Returns:
    bool: True if login was successful, False otherwise.
    """
    return response.url == expected_response

def write_to_file(data, filename, jsonify=False, html=False):
    """
    Writes given data to a file in a formatted key-value pair style or as JSON/HTML.
    Parameters:
    data: Data to be written to the file.
    filename (str): The name of the file where data will be written.
    jsonify (bool): If True, saves data as JSON. Default is False.
    html (bool): If True, saves data as HTML. Default is False.
    Returns:
    None
    """
    if html:
        with open(filename, "w") as html_file:
            html_file.write(data)
    elif jsonify:
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
    else:
        with open(filename, 'w') as file:
            for key, value in data.items():
                file.write(f"{key.upper()}\n")
                file.write("-" * (len(key) + 10) + "\n")
                if isinstance(value, list):
                    for item in value:
                        file.write(f" - {item}\n")
                elif isinstance(value, Tag):
                    file.write(str(value))
                else:
                    file.write(f"{value}\n")
                file.write("\n\n")

# ============================================================
# DATA EXTRACTION FUNCTIONS
# Functions that handle the extraction of data from web pages.
# ============================================================

def extract_crawl_data(soup, url):
    """
    Extracts data from the BeautifulSoup object created from the crawled URL.
    Parameters:
    soup (BeautifulSoup): BeautifulSoup object of the crawled page.
    url (str): The URL being crawled.
    Returns:
    dict: Extracted data from the crawled URL.
    """
    favicon_tag = soup.find("link", {"rel": "icon"})
    meta_description_tag = soup.find("meta", {"name": "description"})
    title_tag = soup.find("title")
    og_tags = [str(tag) for tag in soup.find_all("meta", property=lambda x: x and x.startswith("og:"))]
    twitter_tags = [str(tag) for tag in soup.find_all("meta", attrs={"name": lambda x: x and x.startswith("twitter:")})]
    canonical_tag = soup.find("link", {"rel": "canonical"})
    internal_links, external_links = extract_links(soup, url)
    images = [img['src'] for img in soup.find_all('img', src=True)]

    return {
        'favicon': favicon_tag.get("href") if favicon_tag else None,
        'meta_description': meta_description_tag.get("content") if meta_description_tag else None,
        'title': title_tag.get_text() if title_tag else None,
        'open_graph_tags': og_tags,
        'twitter_card_tags': twitter_tags,
        'canonical_url': canonical_tag.get("href") if canonical_tag else None,
        'internal_links': internal_links,
        'external_links': external_links,
        'image_urls': images,
        'sitemap_urls': parse_sitemap(url)
    }

def extract_content_data(soup):
    """
    Extracts main content data from the BeautifulSoup object.
    Parameters:
    soup (BeautifulSoup): BeautifulSoup object of the crawled page.
    Returns:
    dict: Extracted main content data.
    """
    meta_description_tag = soup.find("meta", {"name": "description"})
    title_tag = soup.find("title")
    paragraphs = [p.get_text().strip() for p in soup.find_all('p')]
    headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    lists = [ul.get_text().strip() for ul in soup.find_all(['ul', 'ol'])]

    return {
        'meta_description': meta_description_tag.get("content") if meta_description_tag else None,
        'title': title_tag.get_text() if title_tag else None,
        'paragraphs': paragraphs,
        'headings': headings,
        'lists': lists
    }

def extract_links(soup, base_url):
    """
    Extracts all internal and external links from the BeautifulSoup object.
    Parameters:
    soup (BeautifulSoup): BeautifulSoup object of the crawled page.
    base_url (str): The base URL of the site being crawled.
    Returns:
    tuple: A tuple containing two lists - internal links and external links.
    """
    internal_links = []
    external_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/'):
            internal_links.append(urljoin(base_url, href))
        elif href.startswith('http'):
            external_links.append(href)
    return internal_links, external_links

def parse_sitemap(url):
    """
    Parses the sitemap of a given URL and returns the list of URLs found in it.
    Parameters:
    url (str): The base URL whose sitemap is to be parsed.
    Returns:
    list: A list of URLs found in the sitemap.
    """
    sitemap_url = url + "/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            return [element.text for element in soup.find_all("loc")]
    except requests.exceptions.RequestException:
        return []

# ============================================================
# DISPLAY FUNCTIONS
# Functions for displaying data.
# ============================================================

def display_crawl_data(data):
    """
    Displays the crawled data in a tabular format using the Rich library.
    Parameters:
    data (dict): The data to be displayed.
    Returns:
    None
    """
    console = Console()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Key", style="dim", width=22)
    table.add_column("Value", overflow="fold")

    for key, value in data.items():
        if isinstance(value, list):
            value = ', '.join(value)
        table.add_row(key.capitalize(), textwrap.fill(str(value), width=80))
    console.print(table)

def display_seo_analysis_results(images_without_alt, broken_links, url):
    """
    Displays the results of the SEO analysis in a tabular format.
    Parameters:
    images_without_alt (list): List of images without alt attributes.
    broken_links (list): List of broken internal links.
    url (str): URL of the analyzed webpage.
    """
    with tqdm(total=100, desc=f'Yirabot SEO Analysis: {url}') as pbar:
        for _ in range(100):
            time.sleep(0.01)
            pbar.update(1)

    console = Console()
    table = Table(title="SEO Analysis Results", show_header=True, header_style="bold blue")
    table.add_column("Type", style="dim", width=15)
    table.add_column("Count", justify="right")
    table.add_column("Details", overflow="fold")

    table.add_row("Images w/o Alt", str(len(images_without_alt)),
                  "\n".join(img['src'] for img in images_without_alt[:5]))
    table.add_row("Broken Links", str(len(broken_links)),
                  "\n".join(broken_links[:5]))

    console.print(table)

# ============================================================
# CRAWLING AND ANALYSIS FUNCTIONS
# Core functions for crawling web pages and specific analyses.
# ============================================================


def crawl(url, extract=False, extract_json=False, session=None):
    """
    Crawls a given URL and extracts various information such as metadata, links, and images.
    Parameters:
    url (str): The URL to be crawled.
    extract (bool): If True, extracts data to a file. Defaults to False.
    extract_json (bool): If True, extracts data to a JSON file. Defaults to False.
    session (Session, optional): Requests session for authenticated crawling.
    Returns:
    None
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        if not is_allowed_by_robots_txt(url):
            print("YiraBot: Crawling forbidden by robots.txt")
            return

        response = session.get(url, headers=headers) if session else requests.get(url, headers=headers)
        dynamic_delay(response)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, features="html5lib")
        data = extract_crawl_data(soup, url)

        if extract or extract_json:
            save_crawl_data(data, url, extract, extract_json)
            return

        display_crawl_data(data)
    except HTTPError as e:
        print(f"YiraBot: HTTP error occurred: {e}")
    except ConnectionError:
        print("YiraBot: Connection error occurred")
    except Timeout:
        print("YiraBot: Timeout error occurred")
    except RequestException:
        print("YiraBot: An error occurred during the request")
    except Exception as e:
        print(f"YiraBot: An unexpected error occurred: {e}")

def crawl_content(url, extract=False, extract_json=False, session=None):
    """
    Specifically crawls a URL for its main content like paragraphs, headings, and lists.
    Parameters:
    url (str): The URL to be crawled for content.
    extract (bool): If True, extracts data to a file. Defaults to False.
    extract_json (bool): If True, extracts data to a JSON file. Defaults to False.
    session (Session, optional): Requests session for authenticated crawling.
    Returns:
    None
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        if not is_allowed_by_robots_txt(url):
            print("YiraBot: Crawling forbidden by robots.txt")
            return

        response = session.get(url, headers=headers) if session else requests.get(url, headers=headers)
        dynamic_delay(response)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, features="html5lib")
        data = extract_content_data(soup)

        if extract or extract_json:
            save_crawl_data(data, url, extract, extract_json)
            return

        display_crawl_data(data)
    except HTTPError as e:
        print(f"YiraBot: HTTP error occurred: {e}")
    except ConnectionError:
        print("YiraBot: Connection error occurred")
    except Timeout:
        print("YiraBot: Timeout error occurred")
    except RequestException:
        print("YiraBot: An error occurred during the request")
    except Exception as e:
        print(f"YiraBot: An unexpected error occurred: {e}")

def crawl_protected_page():
    """
    Handles the crawling of protected web pages that require authentication.
    """
    session = requests.Session()
    print("YiraBot: Session Started.")

    # Function to handle the login process
    def login():
        login_url = input("Enter the login page URL: ")
        if login_url.startswith("http://"):
            sys.exit(f"YiraBot: Cannot use authentication on HTTP websites, Not Secure.")
        if not login_url.startswith("https://"):
            login_url = "https://" + login_url

        expected_response = input("Enter the success redirect URL: ")
        if "/" not in expected_response:
            expected_response += "/"
        if not expected_response.startswith("https://"):
            expected_response = "https://" + expected_response

        username_field = input("Enter the username form input name: ")
        password_field = input("Enter the password form input name: ")
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")

        return login_url, expected_response, {
            username_field: username,
            password_field: password
        }

    # Attempt to login
    try:
        login_url, expected_response, credentials = login()
        response = session.post(login_url, data=credentials)
        response.raise_for_status()
    except HTTPError as e:
        print(f"Login failed, HTTP error: {e}")
        return
    except ConnectionError:
        print("Login failed, connection error.")
        return
    except Timeout:
        print("Login failed, timeout error.")
        return
    except RequestException:
        print("Login failed, request error.")
        return

    # Check if login was successful
    if not login_successful(response, expected_response):
        print("Login failed, please check your credentials.")
        return

    print(f"YiraBot: Successfully logged into {extract_domain(login_url)}")
    print("YiraBot: Use CTRL-C to stop session.")

    # Crawling loop for protected pages
    while True:
        try:
            protected_url = input("Enter the URL of the protected page: ")
            if protected_url.startswith("http://"):
                print(f"YiraBot: Cannot use authentication on HTTP websites, Not Secure.")
                continue
            if not protected_url.startswith("https://"):
                protected_url = "https://" + protected_url

            crawl_choice = input("- Select Crawl Method:\n1: Basic Crawl\n2: Content Crawl\n3: Check Crawl\nInput: ")
            crawl_choice = int(crawl_choice)
            if crawl_choice == 1:
                crawl(protected_url, session=session)
            elif crawl_choice == 2:
                crawl_content(protected_url, session=session)
            elif crawl_choice == 3:
                seo_error_analysis(protected_url, session=session)
            else:
                print("YiraBot: Unexpected Input.")
        except ValueError:
            print("YiraBot: Please enter a valid number for crawl choice.")
        except KeyboardInterrupt:
            print("\nYiraBot: Session Stopped")
            break
def get_html(url):
    """
    Downloads the complete HTML of the specified URL and saves it as a file.
    Parameters:
    url (str): URL of the webpage to download.
    """
    try:
        response = requests.get(url)
        html = response.text
        safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"{safe_url}.{timestamp}.html"

        write_to_file(html, filename, html=True)

        print(f"YiraBot: HTML file '{filename}' created.")
    except Exception as e:
        print(f"YiraBot Error: An error occurred while trying to get HTML. {e}")


# ============================================================
# SEO ANALYSIS FUNCTIONS
# Functions dedicated to performing SEO analysis.
# ============================================================

def seo_error_analysis(url, session=None):
    """
    Performs an SEO error analysis on the specified webpage.
    Checks for common SEO pitfalls such as images without 'alt' attributes and broken internal links.
    Parameters:
    url (str): URL of the webpage to analyze.
    session (Session, optional): Session object for authenticated requests.
    """
    try:
        response = session.get(url) if session else requests.get(url)
        dynamic_delay(response)
        soup = BeautifulSoup(response.content, 'html.parser')

        images_without_alt = [img for img in soup.find_all('img') if not img.get('alt')]
        broken_links = []
        for link in soup.find_all('a', href=True):
            link_url = link['href']
            if not link_url.startswith(('http', '#', 'mailto:')):
                full_url = urljoin(url, link_url)
                try:
                    link_response = requests.head(full_url)
                    if link_response.status_code >= 400:
                        broken_links.append(full_url)
                except requests.RequestException:
                    broken_links.append(full_url)

        display_seo_analysis_results(images_without_alt, broken_links, url)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during SEO analysis: {e}")
    except KeyboardInterrupt or EOFError:
        sys.exit("YiraBot: SEO Analysis Aborted")

# ============================================================
# SAVING DATA FUNCTIONS
# Functions that handle saving the crawled data.
# ============================================================

def save_crawl_data(data, url, extract, extract_json):
    """
    Saves the crawled data to a file in text or JSON format.
    Parameters:
    data (dict): The data to be saved.
    url (str): The URL of the crawled site.
    extract (bool): Whether to save data in text format.
    extract_json (bool): Whether to save data in JSON format.
    Returns:
    None
    """
    safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"{safe_url}.{timestamp}"

    if extract:
        write_to_file(data, f"{filename}.txt")
        print("YiraBot: Text file created.")
    if extract_json:
        write_to_file(data, f"{filename}.json", jsonify=True)
        print("YiraBot: JSON file created.")
