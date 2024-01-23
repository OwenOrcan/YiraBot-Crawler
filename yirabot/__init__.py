import sys
import requests
from bs4 import BeautifulSoup, Tag
import textwrap
import urllib.robotparser
from urllib import error

class Yirabot:
    def get_html(self, url):
        """
          Retrieves the HTML content of a given URL.

          Parameters:
          url (str): The URL of the webpage to be fetched.

          Returns:
          str: The HTML content of the webpage. Returns None if an error occurs.
          """
        try:
            response = requests.get(url)
            return response.text
        except Exception as e:
            print(f"YiraBot Error: An error occured while trying to get hmtl. {e}")
            return

    def is_allowed_by_robots_txt(self,url):
        """
        Checks if the given URL is allowed to be crawled based on its robots.txt file.

        Parameters:
        url (str): The URL to check against the robots.txt file.

        Returns:
        bool: True if crawling is allowed, False otherwise.
        """
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(url + "/robots.txt")
        rp.read()
        return rp.can_fetch("*", url)

    def parse_sitemap(self, url):
        """
        Parses the sitemap of a given website to find URLs.

        Parameters:
        url (str): The base URL of the website whose sitemap is to be parsed.

        Returns:
        list: A list of URLs found in the sitemap. Returns an empty list if an error occurs or sitemap is not found.
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

    def crawl(self, url):
        """
        Crawls a given URL and extracts various information such as favicon, meta description, title, tags, and links.

        Parameters:
        url (str): The URL of the website to be crawled.

        Returns:
        dict: A dictionary containing extracted information from the webpage. Returns None if an error occurs or crawling is forbidden.
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

            if not self.is_allowed_by_robots_txt(url):
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
                sitemap_urls = self.parse_sitemap(url)

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

                return data

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

    def crawl_content(self, url):
        """
        Crawls a given URL and extracts detailed content like paragraphs, headings, and lists.

        Parameters:
        url (str): The URL of the website whose content is to be extracted.

        Returns:
        dict: A dictionary containing extracted content from the webpage. Returns None if an error occurs or crawling is forbidden.
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

            if not self.is_allowed_by_robots_txt(url):
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


                data = {
                    'meta_description': meta_description_tag.get("content") if meta_description_tag else None,
                    'title': title_tag.get_text() if title_tag else None,
                    'image_urls': image_urls,
                    'paragraphs': paragraphs,
                    'headings': headings,
                    'lists': lists
                }

                return data

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


