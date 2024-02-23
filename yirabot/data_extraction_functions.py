from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


def extract_crawl_data(soup, url):
    """
    Extracts data from a BeautifulSoup object created from a crawled URL, including metadata,
    social media tags, links, and images.

    Parameters:
    - soup (BeautifulSoup): BeautifulSoup object of the crawled page.
    - url (str): The URL being crawled.

    Returns:
    - dict: A dictionary with the extracted data, including favicon, meta description, title,
      open graph tags, Twitter card tags, canonical URL, internal and external links, image URLs,
      and sitemap URLs.
    """
    # Extract favicon, meta description, and title
    favicon_tag = soup.find("link", {"rel": "icon"})
    meta_description_tag = soup.find("meta", {"name": "description"})
    title_tag = soup.find("title")

    # Extract Open Graph and Twitter card tags
    og_tags = [str(tag) for tag in soup.find_all("meta", property=lambda x: x and x.startswith("og:"))]
    twitter_tags = [str(tag) for tag in soup.find_all("meta", attrs={"name": lambda x: x and x.startswith("twitter:")})]

    # Extract canonical URL
    canonical_tag = soup.find("link", {"rel": "canonical"})

    # Extract internal and external links
    internal_links, external_links = extract_links(soup, url)

    # Extract image URLs
    images = [img['src'] for img in soup.find_all('img', src=True)]

    # Compile extracted data into a dictionary
    extracted_data = {
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

    return extracted_data


def extract_content_data(soup):
    """
    Extracts main content data from a BeautifulSoup object, including titles, paragraphs,
    headings, and lists.

    Parameters:
    - soup (BeautifulSoup): BeautifulSoup object of the crawled page.

    Returns:
    - dict: A dictionary with the extracted main content data.
    """
    # Extract title, paragraphs, headings, and lists
    title_tag = soup.find("title")
    paragraphs = [p.get_text().strip() for p in soup.find_all('p')]
    headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    lists = [ul.get_text().strip() for ul in soup.find_all(['ul', 'ol'])]

    # Compile extracted content into a dictionary
    content_data = {
        'title': title_tag.get_text() if title_tag else None,
        'paragraphs': paragraphs,
        'headings': headings,
        'lists': lists
    }

    return content_data


def extract_links(soup, base_url):
    """
    Extracts all internal and external links from a BeautifulSoup object and categorizes them.

    Parameters:
    - soup (BeautifulSoup): BeautifulSoup object of the crawled page.
    - base_url (str): The base URL for resolving relative links.

    Returns:
    - tuple: A tuple containing two lists, the first with internal links and the second with external links.
    """
    internal_links = []
    external_links = []

    # Normalize the base URL to prevent duplication issues
    base_url = base_url.rstrip('/') + '/'

    for link in soup.find_all('a', href=True):
        href = link['href'].split('#')[0]  # Remove URL fragments
        href = href.split('?')[0]  # Remove URL query parameters

        # Categorize and normalize links
        if href.startswith('/'):
            full_link = urljoin(base_url, href.lstrip('/'))
            internal_links.append(full_link)
        elif href.startswith('http') or href.startswith('https'):
            external_links.append(href)

    return internal_links, external_links


def parse_sitemap(url, script=False):
    """
    Parses the sitemap of a given URL to extract and return all contained URLs.
    If 'script' is True, the 'url' parameter is treated as the full sitemap link.

    Parameters:
    - url (str): The URL to the sitemap if 'script' is True, or the base URL whose sitemap is to be parsed.
    - script (bool): Indicates whether the provided URL is the direct link to the sitemap.

    Returns:
    - list: A list of URLs found in the sitemap. If no sitemap is found, returns an
            appropriate message.
    """
    if script:
        # Directly use the provided URL for the sitemap
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                return [element.text for element in soup.find_all("loc")]
        except requests.exceptions.RequestException:
            return []
    else:
        # Standard sitemap URLs
        sitemap_urls = [url + "/sitemap.xml", url + "/static/sitemap.xml"]

        # Attempt to parse standard sitemaps
        for sitemap_url in sitemap_urls:
            try:
                response = requests.get(sitemap_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'xml')
                    return [element.text for element in soup.find_all("loc")]
            except requests.exceptions.RequestException:
                continue  # Proceed to next URL on failure

        return []
