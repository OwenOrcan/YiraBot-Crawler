from .help import help
from .crawling_functions import *


def main():
    """
    Main function to handle command line arguments and orchestrate the execution
    of commands based on user input.
    """
    if len(sys.argv) < 2:
        help()
    elif len(sys.argv) > 4:
        sys.exit("YiraBot: Too many arguments!")
    else:
        command = sys.argv[1].lower()
        argument = sys.argv[2] if len(sys.argv) > 2 else None
        process_command(command, argument)


def process_command(command, argument):
    """
    Processes the given command with an optional argument, directing to the appropriate action.
    """
    if command == "session":
        crawl_protected_page()
    elif command in ["get-html", "seo"]:
        process_url_command(command, argument)
    elif command in ["crawl", "scrape"]:
        process_crawl_command(command, argument)
    else:
        print("YiraBot: Unknown command.")


def process_url_command(command, argument):
    """
    Handles commands that operate on a single URL, such as downloading HTML or performing SEO analysis.
    """
    if not argument:
        sys.exit("YiraBot: A URL is required for this command.")
    try:
        url = validate_url(argument)
        if command == "get-html":
            get_html(url)
        elif command == "seo":
            seo_error_analysis(url)
    except Exception as e:
        sys.exit(f"YiraBot: Error occurred: {e}")


def process_crawl_command(command, argument):
    """
    Processes commands related to crawling or scraping, handling optional flags for output format and mobile user-agent.
    """
    if not argument:
        sys.exit("YiraBot: A URL is required for this command.")
    url = validate_url(argument)
    flag = sys.argv[3] if len(sys.argv) == 4 else None

    extract = flag == "-file"
    extract_json = flag == "-json"
    mobile = flag == "-mobile"

    if command == "crawl":
        crawl(url, extract=extract, extract_json=extract_json, mobile=mobile)
    elif command == "scrape":
        crawl_content(url, extract=extract, extract_json=extract_json)


def validate_url(url):
    """
    Ensures the URL starts with a proper scheme (http or https) and prepends "https://" if missing.
    """
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


if __name__ == '__main__':
    main()
