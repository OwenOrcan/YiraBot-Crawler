import json
import re
import sys
import time
import urllib.robotparser
from bs4 import Tag
from rich import print
import random

# ============================================================
# UTILITY FUNCTIONS
# General-purpose functions used across the script.
# ============================================================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)",
    "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
]
MOBILE_USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.92 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366",
]
def extract_domain(url,):
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

def dynamic_delay(response, script=False):
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
            if not script:
                print("YiraBot: Website Server Is Overwhelmed, Waiting Before Starting Crawl.")
            time.sleep(retry_after)
        else:
            if not script:
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

def get_random_user_agent(mobile=False):
    """
    Selects a random user agent from the list.
    Returns:
        str: A randomly selected user agent.
    """
    if mobile:
        return random.choice(MOBILE_USER_AGENTS)
    return random.choice(USER_AGENTS)