from colorama import Fore



def help():
    HELP_MESSAGE = Fore.RED + """
YiraBot Web Crawler v1.0.7.3.1
----------------------------------
Command Line Web Crawling and SEO Analysis Tool""" + Fore.MAGENTA + """

Usage:
    yirabot [command] <url> [flag] 

Commands:""" + Fore.CYAN + """

crawl
    - Basic Crawl: Performs a standard crawl of the specified URL.
    - Flags:
        -file: Saves data to a text file.
        -json: Saves data to a JSON file.

check
    - SEO Analysis: Analyzes SEO-related elements of the specified URL.

crawl-content
    - Content Crawl: Extracts main content from the specified URL.
    - Flags:
        -file: Saves content data to a text file.
        -json: Saves content data to a JSON file.

get-html
    - HTML Copy: Downloads and saves the complete HTML of the specified URL.

session
    - Protected Crawl: Starts a session for crawling authenticated pages.

""" + Fore.LIGHTBLUE_EX + """
For detailed documentation and examples, visit:
https://github.com/OwenOrcan/YiraBot-Crawler
    """ + Fore.RESET
    print(HELP_MESSAGE)