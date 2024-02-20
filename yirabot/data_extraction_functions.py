from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

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
    title_tag = soup.find("title")
    paragraphs = [p.get_text().strip() for p in soup.find_all('p')]
    headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    lists = [ul.get_text().strip() for ul in soup.find_all(['ul', 'ol'])]

    return {
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
    seo (bool): If True, links are returned without http/https protocols.
    Returns:
    tuple: A tuple containing two lists - internal links and external links.
    """
    internal_links = []
    external_links = []

    # Normalize the base URL to prevent duplication issues
    base_url = base_url.rstrip('/') + '/'

    for link in soup.find_all('a', href=True):
        href = link['href'].split('#')[0]  # Remove URL fragments
        href = href.split('?')[0]  # Remove URL query parameters if not needed for SEO

        if href.startswith('/'):
            full_link = urljoin(base_url, href.lstrip('/'))
            internal_links.append(full_link)
        elif href.startswith('http') or href.startswith('https'):
            external_links.append(href)

    return internal_links, external_links

def parse_sitemap(url, script=False):
    """
    Parses the sitemap of a given URL and returns the list of URLs found in it.
    Parameters:
    url (str): The base URL whose sitemap is to be parsed.
    Returns:
    list: A list of URLs found in the sitemap.
    """
    sitemap_url = url + "/sitemap.xml"
    sitemap_url2 = url + "/static/sitemap.xml"
    if script:
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            return [element.text for element in soup.find_all("loc")]
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            return [element.text for element in soup.find_all("loc")]
        else:
            return ["NO SITEMAP FOUND IN WEBSITE"]
    except Exception:
        response = requests.get(sitemap_url2)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            return [element.text for element in soup.find_all("loc")]
        else:
            return ["NO SITEMAP FOUND IN WEBSITE"]

    except requests.exceptions.RequestException:
        return []