from . import errors
from .seo_functions import *
from .helper_functions import *
from .data_extraction_functions import *
from urllib.error import HTTPError
from requests import RequestException, Timeout
from bs4 import BeautifulSoup
from .data_extraction_functions import parse_sitemap


# noinspection PyUnboundLocalVariable
class Yirabot:
    def __init__(self):
        self.urls = None
        self.sitemap_url = None

    def seo_analysis(self, url, session=None):
        """
        Performs SEO analysis on the given URL, extracting and analyzing various SEO factors.
        """
        headers = {'User-Agent': get_random_user_agent()}
        try:
            response = session.get(url, headers=headers) if session else requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            data = {
                'title_length': analyze_title(soup),
                'meta_desc_length': analyze_meta_description(soup),
                'headings': analyze_headings(soup),
                'images_without_alt': analyze_images_for_alt_text(soup),
                'keyword_results': keyword_analysis(get_combined_text(soup)),
                'is_responsive': check_mobile_responsiveness(url),
                'social_media_integration': check_social_media_integration(url),
                'website_language': check_website_language(url),
            }
            return data

        except ConnectionError:
            raise errors.ConnectionError(url)
        except Timeout:
            raise errors.TimeoutError(url)
        except HTTPError:
            raise errors.HTTPError(response.status_code)
        except RequestException:
            raise errors.RequestError(url)

    def crawl(self, url, session=None, force=False):
        headers = {'User-Agent': get_random_user_agent()}
        try:
            if not force:
                if not is_allowed_by_robots_txt(url):
                    raise errors.RobotsError(url)

            response = session.get(url, headers=headers) if session else requests.get(url, headers=headers, timeout=10)
            dynamic_delay(response, script=True)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, features="html5lib")

            meta_description_tag = soup.find("meta", {"name": "description"})
            favicon_tag = soup.find("link", {"rel": "icon"})
            title_tag = soup.find("title")
            og_tags = [str(tag) for tag in soup.find_all("meta", property=lambda x: x and x.startswith("og:"))]
            twitter_tags = [str(tag) for tag in
                            soup.find_all("meta", attrs={"name": lambda x: x and x.startswith("twitter:")})]
            canonical_tag = soup.find("link", {"rel": "canonical"})
            internal_links, external_links = extract_links(soup, url)
            images = [img['src'] for img in soup.find_all('img', src=True)]

            data = {
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
            if type(data) is None:
                self.crawl(url, session, force) # sometimes the function returns none, when that happens, call that shit again.
            else:
                return data

        except HTTPError:
            raise errors.HTTPError(response.status_code)
        except ConnectionError:
            raise errors.ConnectionError(url)
        except Timeout:
            raise errors.TimeoutError(url)
        except RequestException:
            raise errors.RequestError(url)

    def scrape(self, url, session=None, force=False):
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
            if not force:
                if not is_allowed_by_robots_txt(url):
                    raise errors.RobotsError(url)

            response = session.get(url, headers=headers) if session else requests.get(url, headers=headers, timeout=10)
            dynamic_delay(response, script=True)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, features="html5lib")

            title_tag = soup.find("title")
            paragraphs = [p.get_text().strip() for p in soup.find_all('p')]
            headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
            lists = [ul.get_text().strip() for ul in soup.find_all(['ul', 'ol'])]

            data = {
                'title': title_tag.get_text() if title_tag else None,
                'paragraphs': paragraphs,
                'headings': headings,
                'lists': lists
            }
            if type(data) is None:
                print("Server did not response, trying again.")
                self.scrape(url, session, force)
            else:
                return data

        except HTTPError:
            raise errors.HTTPError
        except ConnectionError:
            raise errors.ConnectionError
        except Timeout:
            raise errors.TimeoutError
        except RequestException:
            raise errors.RequestError

    def validate(self, sitemap_url):
        self.sitemap_url = sitemap_url
        try:
            self.urls = parse_sitemap(self.sitemap_url, script=True)
        except ConnectionError:
            raise errors.ConnectionError(sitemap_url)
        except HTTPError:
            raise errors.HTTPError(sitemap_url)
        except TimeoutError:
            raise errors.TimeoutError(sitemap_url)
        except RequestException:
            raise errors.RequestError(sitemap_url)
        responses = {}

        for url in self.urls:
            response = requests.head(url, allow_redirects=True, timeout=10)
            response_code = response.status_code
            responses[url] = response_code
        return responses
