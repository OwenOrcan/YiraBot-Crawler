import sys
import requests
from bs4 import BeautifulSoup, Tag
import textwrap
import urllib.robotparser
from datetime import datetime
from urllib import error
from urllib.parse import urljoin
from tqdm import tqdm
from rich import print
from rich.table import Table
from rich.console import Console
import time
import json




def seo_error_analysis(url):
    """
    Performs an SEO error analysis on the specified webpage.

    This function conducts a thorough check for common SEO pitfalls on the given webpage.
    It specifically looks for:
    - Images without 'alt' attributes, which are essential for SEO and accessibility.
    - Broken internal links, which negatively impact the user experience and site's SEO ranking.
    """
    try:
        response = requests.get(url)
        dynamic_delay(response)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Images without alt tags
        images_without_alt = [img for img in soup.find_all('img') if not img.get('alt')]

        # Broken internal links
        broken_links = []
        for link in soup.find_all('a', href=True):
            link_url = link['href']
            if not link_url.startswith('http') and not link_url.startswith('#') and not link_url.startswith('mailto:'):
                full_url = urljoin(url, link_url)
                try:
                    link_response = requests.head(full_url)
                    if link_response.status_code >= 400:
                        broken_links.append(full_url)
                except requests.RequestException:
                    broken_links.append(full_url)

        with tqdm(total=100, desc=f'Yirabot Crawling: {url}') as pbar:
            for _ in range(100):
                time.sleep(0.01)
                pbar.update(1)

        # Printing Results in Table Format
        console = Console()
        table = Table(title="SEO Analysis Results", show_header=True, header_style="bold blue")
        table.add_column("Type", style="dim", width=15)
        table.add_column("Count", justify="right")
        table.add_column("Details", overflow="fold")

        table.add_row("Images w/o Alt", str(len(images_without_alt)),
                      "\n".join(img['src'] for img in images_without_alt[:5]))
        table.add_row("Broken Links", str(len(broken_links)),
                      "\n".join(broken_links))

        console.print(table)

    except requests.exceptions.RequestException as e:
        print(f"Error occurred during SEO analysis: {e}")
    except KeyboardInterrupt or EOFError:
        sys.exit("YiraBot: Crawl Aborted")

def dynamic_delay(response):
    """
    Dynamically delays the next request based on the server's response.
    """
    try:
        if response.status_code == 429:
            try:
                retry_after = int(response.headers.get("Retry-After", 10))
            except ValueError:
                retry_after = 10  # Fallback if the header is not an integer
            print("YiraBot: Website Server Is Overwhelmed, Waiting Before Starting Crawl.")
            time.sleep(retry_after)
        else:
            print("YiraBot: Starting Crawl.")
            time.sleep(1)  # Default delay for non-429 responses
    except KeyboardInterrupt or EOFError:
        sys.exit("YiraBot: Crawl Aborted")

def get_html(url):
    try:
        response = requests.get(url)
        html = response.text

        safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")

        timestamp = datetime.now().strftime("%Y-%m-%d")

        filename = f"{safe_url}.{timestamp}.html"

        with tqdm(total=100, desc=f'Yirabot Crawling: {url}') as pbar:
            for _ in range(100):
                time.sleep(0.001)
                pbar.update(1)


        write_to_file(html, filename, html=True)

        sys.exit("YiraBot: HTML file created.")

    except Exception as e:
        print(f"YiraBot Error: An error occured while trying to get html. {e}")
        return

def write_to_file(data, filename, jsonify=False, html=False):
    """
    Writes given data to a file in a formatted key-value pair style.

    Parameters:
    data (dict): A dictionary containing the data to be written.
    filename (str): The name of the file where data will be written.

    Returns:
    None
    """

    if html:
        with open(filename, "w") as html_file:
            html_file.write(data)
            return

    if jsonify:
        with open(filename, "w") as json_file:
           json.dump(data, json_file, indent=4)
           return

    with open(filename, 'w') as file:
        max_key_length = max(len(key) for key in data.keys())  # Find the longest key
        divider = "-" * (max_key_length + 50)  # Adjust the divider length based on the key length
        for key, value in data.items():
            if isinstance(value, list):
                str_values = [str(item) for item in value]
                value = ', '.join(str_values)

            # Format each line as a table row
            formatted_key = key.capitalize().ljust(max_key_length)
            file.write(f"{formatted_key} : {value}\n")
            file.write(f"{divider}\n")

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

def parse_sitemap(url):
    """
    Parses the sitemap of a given URL and returns the list of URLs found in it.

    Parameters:
    url (str): The base URL whose sitemap is to be parsed.

    Returns:
    list: A list of URLs found in the sitemap.
    """
    sitemap_url = url + "/sitemap.xml"
    secondary_url = url + "/static/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response2 = requests.get(secondary_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            urls = [element.text for element in soup.find_all("loc")]
            return urls
        elif response2.status_code == 200:
            soup = BeautifulSoup(response2.content, 'xml')
            urls = [element.text for element in soup.find_all("loc")]
            return urls
    except requests.exceptions.RequestException:
        return []

def crawl(url, extract=False, extract_json=False):
    """
    Crawls a given URL and extracts various information such as metadata, links, and images.

    Parameters:
    url (str): The URL to be crawled.
    extract (bool): If True, extracts data to a file. Defaults to False.

    Returns:
    None
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        if not is_allowed_by_robots_txt(url):
            print("YiraBot: Crawling forbidden by robots.txt")
            return

        try:
            response = requests.get(url, headers=headers)
            dynamic_delay(response)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, features="html5lib")

            favicon_tag = soup.find("link", {"rel": "icon"})
            meta_description_tag = soup.find("meta", {"name": "description"})
            title_tag = soup.find("title")
            og_tags = soup.find_all("meta", property=lambda x: x and x.startswith("og:"))
            twitter_tags = soup.find_all("meta", attrs={"name": lambda x: x and x.startswith("twitter:")})
            canonical_tag = soup.find("link", {"rel": "canonical"})

            links = soup.find_all('a', href=True)
            internal_links = [link['href'] for link in links if link['href'].startswith('/')]
            external_links = [link['href'] for link in links if link['href'].startswith('http')]
            images = soup.find_all('img', src=True)
            image_urls = [img['src'] for img in images]
            sitemap_urls = parse_sitemap(url)

            with tqdm(total=100, desc=f'Yirabot Crawling: {url}') as pbar:
                for _ in range(100):
                    time.sleep(0.01)
                    pbar.update(1)

            data = {
                'favicon': favicon_tag.get("href") if favicon_tag else None,
                'meta_description': meta_description_tag.get("content") if meta_description_tag else None,
                'title': title_tag.get_text() if title_tag else None,
                'open_graph_tags': og_tags,
                'twitter_card_tags': twitter_tags,
                'canonical_url': canonical_tag.get("href") if canonical_tag else None,
                'internal_links': internal_links,
                'external_links': external_links,
                'image_urls': image_urls,
                'sitemap_urls': sitemap_urls
            }


            if extract:
                # Replace problematic characters in the URL
                safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")

                # Format the current timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d")

                # Generate a safe filename
                filename = f"{safe_url}.{timestamp}.txt"

                write_to_file(data, filename)
                sys.exit("YiraBot: file created.")

            if extract_json:
                safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")

                timestamp = datetime.now().strftime("%Y-%m-%d")

                filename = f"{safe_url}.{timestamp}.json"

                write_to_file(data, filename, jsonify=True)

                sys.exit("YiraBot: JSON file created.")




            console = Console()

            table = Table(show_header=True, header_style="bold blue")

            # Add columns with specific style and overflow
            table.add_column("Key", style="dim", width=22)  # Adjust width as needed
            table.add_column("Value", overflow="fold")

            for key, value in data.items():
                if isinstance(value, list):
                    # Convert all items in lists to strings
                    value = ', '.join([str(v) for v in value])
                elif isinstance(value, Tag):
                    # Convert Tag objects to strings
                    value = str(value)

                # Apply specific styling to make different things stand out
                if key == 'title':
                    style = "bold"
                elif "url" in key:
                    style = "italic"
                else:
                    style = ""

                # Add a blank line for separation between different items
                if style:
                    table.add_row(key.capitalize(), str(value), style=style)
                else:
                    table.add_row(key.capitalize(), str(value))
                table.add_row("", "")  # This adds a blank row for better separation

            console.print(table)



        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
        except Exception as e:
            print(f"An error occurred while parsing the page: {e}")

    except urllib.error.URLError as e:
        sys.exit(f"Yirabot:URL exception occured: {e}")
    except KeyboardInterrupt or EOFError:
        sys.exit("YiraBot: Process aborted")

def crawl_content(url, extract=False, extract_json=False):
    """
    Specifically crawls a URL for its main content like paragraphs, headings, and lists.

    Parameters:
    url (str): The URL to be crawled for content.
    extract (bool): If True, extracts data to a file. Defaults to False.

    Returns:
    None
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        if not is_allowed_by_robots_txt(url):
            print("YiraBot: Crawling forbidden by robots.txt")
            return

        try:
            response = requests.get(url, headers=headers)
            dynamic_delay(response)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, features="html5lib")

            meta_description_tag = soup.find("meta", {"name": "description"})
            title_tag = soup.find("title")
            images = soup.find_all('img', src=True)
            image_urls = [img['src'] for img in images]

            paragraphs = [p.get_text().strip() for p in soup.find_all('p')]
            headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
            lists = [ul.get_text().strip() for ul in soup.find_all(['ul', 'ol'])]

            with tqdm(total=100, desc=f'Yirabot Crawling: {url}') as pbar:
                for _ in range(100):
                    time.sleep(0.01)
                    pbar.update(1)

            data = {
                'meta_description': meta_description_tag.get("content") if meta_description_tag else None,
                'title': title_tag.get_text() if title_tag else None,
                'image_urls': image_urls,
                'paragraphs': paragraphs,
                'headings': headings,
                'lists': lists
            }

            if extract:
                safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{safe_url}.{timestamp}.txt"

                write_to_file(data, filename)
                sys.exit("YiraBot: file created.")

            if extract_json:
                safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")

                timestamp = datetime.now().strftime("%Y-%m-%d")

                filename = f"{safe_url}.{timestamp}.json"

                write_to_file(data, filename, jsonify=True)

                sys.exit("YiraBot: JSON file created.")


            console = Console()
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Key", style="dim", width=22)
            table.add_column("Value", overflow="fold")

            for key, value in data.items():
                if isinstance(value, list):
                    value = ', '.join([str(v) for v in value])
                table.add_row(key.capitalize(), textwrap.fill(str(value), width=80))
                table.add_row("", "")  # This adds a blank row for better separation

            console.print(table)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
        except Exception as e:
            print(f"An error occurred while parsing the page: {e}")
    except urllib.error.URLError:
        sys.exit(f"YiraBot: Url is invalid. {url}")
    except KeyboardInterrupt or EOFError:
        sys.exit("YiraBot: Process aborted")

