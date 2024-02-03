from .helper_functions import *
from .data_extraction_functions import *
from urllib.error import HTTPError
from requests import RequestException, Timeout
from bs4 import BeautifulSoup

"""
YiraBot's Python Module Integration.

Still Under Development
"""




class Crawler:
    def crawl(self,url,session=None):
        headers = {'User-Agent': get_random_user_agent()}
        try:
            if not is_allowed_by_robots_txt(url):
                print("YiraBot: Crawling forbidden by robots.txt")
                return

            response = session.get(url, headers=headers) if session else requests.get(url, headers=headers)
            dynamic_delay(response, script=True)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, features="html5lib")

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


    def scrape(self, url, session=None):
        """
        Specifically crawls a URL for its main content like paragraphs, headings, and lists.
        Parameters:
        url (str): The URL to be crawled for content.
        session (Session, optional): Requests session for authenticated crawling.
        Returns:
        Data: Dict
        """
        headers = {'User-Agent': get_random_user_agent()}
        try:
            if not is_allowed_by_robots_txt(url):
                print("YiraBot: Crawling forbidden by robots.txt")
                return

            response = session.get(url, headers=headers) if session else requests.get(url, headers=headers)
            dynamic_delay(response, script=True)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, features="html5lib")

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

