import sys
import requests
from bs4 import BeautifulSoup, Tag
import textwrap
import urllib.robotparser
from datetime import datetime
from urllib import error
from tqdm import tqdm
from rich import print
from rich.table import Table
from rich.console import Console
import time



def write_to_file(data, filename):
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
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url + "/robots.txt")
    rp.read()
    return rp.can_fetch("*", url)

def parse_sitemap(url):
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

def crawl(url, extract=False):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 ...'}

        if not is_allowed_by_robots_txt(url):
            print("YiraBot: Crawling forbidden by robots.txt")
            return

        try:
            response = requests.get(url, headers=headers)
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
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                # Generate a safe filename
                filename = f"{safe_url}.{timestamp}.txt"

                write_to_file(data, filename)
                sys.exit("YiraBot: file created.")

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

    except urllib.error.URLError:
        sys.exit(f"Yirabot: Url is invalid. {url}")
    except KeyboardInterrupt or EOFError:
        sys.exit("YiraBot: Process aborted")


def crawl_content(url, extract=False):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 ...'}

        if not is_allowed_by_robots_txt(url):
            print("YiraBot: Crawling forbidden by robots.txt")
            return

        try:
            response = requests.get(url, headers=headers)
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
                    time.sleep(0.01)  # Adjust this as needed
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



