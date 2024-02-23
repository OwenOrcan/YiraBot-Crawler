import re
from collections import Counter, defaultdict
from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup
from rich import print
from .display_functions import display_seo_results

# ============================================================
# SEO ANALYSIS FUNCTIONS
# Functions dedicated to performing SEO analysis.
# ============================================================
STOPWORDS = set(
    ["a", "an", "the", "and", "or", "in", "of", "by", "for", "with", "on", "at", "to", "from", "up", "down", "in",
     "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why",
     "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only",
     "own", "same", "so", "than", "too", "very", "your", "that"])


def check_website_language(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        html_tag = soup.find('html')
        if html_tag and 'lang' in html_tag.attrs:
            language = html_tag.attrs['lang']
            return language
        else:
            return "Language attribute not found"
    except requests.exceptions.RequestException as e:
        return f"Error occurred: {e}"


def check_social_media_integration(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        social_media = {
            "Facebook": False,
            "Twitter": False,
            "Instagram": False,
            "LinkedIn": False,
            "YouTube": False
        }

        for link in soup.find_all('a', href=True):
            href = link['href']
            if "facebook.com" in href:
                social_media["Facebook"] = True
            elif "twitter.com" in href:
                social_media["Twitter"] = True
            elif "instagram.com" in href:
                social_media["Instagram"] = True
            elif "linkedin.com" in href:
                social_media["LinkedIn"] = True
            elif "youtube.com" in href:
                social_media["YouTube"] = True

        return social_media
    except requests.exceptions.RequestException as e:
        return {"Error": str(e)}


def check_mobile_responsiveness(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        viewport_meta = soup.find("meta", {"name": "viewport"})

        if viewport_meta and "width=device-width" in viewport_meta.get("content", ""):
            return True, "Mobile Responsive"
        else:
            return False, "Not Mobile Responsive"
    except requests.exceptions.RequestException as e:
        return False, f"Error occurred: {e}"


def check_link_status(url, session=None):
    """
    Checks the status of a link.
    Returns a tuple of (is_broken, status_code, reason).
    """
    try:
        response = session.head(url, allow_redirects=True) if session else requests.head(url, allow_redirects=True)
        if response.status_code == 404:
            return True, 404, "Not Found"
        elif 300 <= response.status_code < 400:
            return True, response.status_code, "Unexpected Redirect"
        return False, response.status_code, "OK"
    except requests.RequestException as e:
        return True, None, f"Error: {e}"


def keyword_analysis(text):
    """
    Analyzes the text for the most frequent non-stopwords.
    """
    words = re.findall(r'\w+', text.lower())
    filtered_words = [word for word in words if word not in STOPWORDS]
    word_counts = Counter(filtered_words)
    return word_counts.most_common(5)


def is_seo_friendly_url(url):
    """
    Determines if the given URL is SEO-friendly based on common best practices.
    Returns a tuple (is_friendly, reason).
    """
    decoded_url = unquote(url)

    if len(decoded_url) > 75:
        return False, "URL is too long (>75 characters)"
    if '_' in decoded_url:
        return False, "URL contains underscores instead of hyphens"

    if not re.match(r'^[a-z0-9\.-]+[a-z0-9/-]*$', decoded_url):
        return False, "URL contains invalid characters"

    if '?' in decoded_url or '&' in decoded_url:
        return False, "URL contains excessive parameters"

    return True, "SEO-friendly"


def analyze_title(soup):
    title_tag = soup.find('title')
    title_length = len(title_tag.get_text()) if title_tag else 0
    if title_length == 0:
        return 0, "Missing or Empty"
    return title_length, "Too Long (Max 60)" if title_length > 60 else "OK"


def analyze_meta_description(soup):
    meta_description_tag = soup.find("meta", {"name": "description"})
    meta_desc_length = len(meta_description_tag.get("content")) if meta_description_tag else 0
    if meta_desc_length == 0:
        return 0, "Missing or Empty"
    return meta_desc_length, "Too Long (Max 300)" if meta_desc_length > 300 else "OK"


def analyze_headings(soup):
    headings = defaultdict(int)
    heading_sequence = []
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        headings[heading.name] += 1
        heading_sequence.append(heading.name)

    return headings, evaluate_heading_structure(headings, heading_sequence)


def evaluate_heading_structure(headings, heading_sequence):
    if 'h1' not in headings or headings['h1'] > 1:
        return "Improper Usage of H1 Tags"

    last_heading_level = 0
    for heading in heading_sequence:
        current_level = int(heading[1])
        if current_level > last_heading_level + 1:
            return f"Jump in heading levels detected at {heading}"
        last_heading_level = current_level

    return "OK"


def analyze_images_for_alt_text(soup):
    images = soup.find_all('img')
    return [img['src'] for img in images if img.get('alt') is None]


def seo_error_analysis(url, session=None):
    try:
        print("YiraBot: Starting SEO Analysis")
        response = session.get(url) if session else requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        title_length, title_status = analyze_title(soup)
        meta_desc_length, meta_desc_status = analyze_meta_description(soup)
        headings, heading_structure_status = analyze_headings(soup)
        images_without_alt = analyze_images_for_alt_text(soup)

        # Combine texts for keyword analysis
        combined_text = get_combined_text(soup)
        keyword_results = keyword_analysis(combined_text)

        # Mobile Responsiveness Check
        is_responsive, responsiveness_message = check_mobile_responsiveness(url)

        # Social Media Integration Check
        social_media_integration = check_social_media_integration(url)

        # Language Check
        website_language = check_website_language(url)

        # Display results
        display_seo_results(
            title_length, title_status,
            meta_desc_length, meta_desc_status,
            keyword_results,
            headings, heading_structure_status,
            images_without_alt,
            is_responsive, responsiveness_message,
            social_media_integration,
            website_language
        )

    except requests.exceptions.RequestException as e:
        print(f"Error occurred during SEO analysis: {e}")


def get_combined_text(soup):
    title_text = soup.find('title').get_text() if soup.find('title') else ""
    meta_description_text = soup.find("meta", {"name": "description"}).get("content", "") if soup.find("meta", {
        "name": "description"}) else ""
    headings_text = ' '.join([h.get_text() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
    return title_text + " " + meta_description_text + " " + headings_text
