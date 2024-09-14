RED = "\033[31m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"
CYAN = "\033[36m"
LIGHTBLUE_EX = "\033[94m"
RESET = "\033[0m"

def help():
    help_message = RED + """
YiraBot Web Crawler v1.0.9 
----------------------------------
Command Line Web Crawling, Web Scraping and SEO Analysis Tool""" + MAGENTA + """

Usage:
    yirabot [command] <url> [flag] """ + WHITE + """

Commands:""" + CYAN + """

crawl
    - Crawl: Performs a standard crawl of the specified URL.
    - Flags:
        -file: Saves data to a text file.
        -json: Saves data to a JSON file.
        -mobile: Uses a mobile User Agent to crawl

seo
    - SEO Analysis: Analyzes SEO-related elements of the specified URL.

scrape
    - Scrape: Extracts main content from the specified URL.
    - Flags:
        -file: Saves content data to a text file.
        -json: Saves content data to a JSON file.
        -mobile: Uses a mobile User Agent to scrape

get-html
    - HTML Copy: Downloads and saves the complete HTML of the specified URL.

session
    - Protected Crawl: Starts a session for crawling authenticated pages.

""" + LIGHTBLUE_EX + """
For detailed documentation and examples, visit:
https://github.com/OwenOrcan/YiraBot-Crawler
    """ + RESET
    print(help_message)
