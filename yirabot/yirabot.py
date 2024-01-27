import sys
from .crawl import crawl, crawl_content, get_html, seo_error_analysis, crawl_protected_page
from .help import help

def main():
    """
    Main function to handle command line arguments and trigger appropriate actions.
    """
    if len(sys.argv) < 2:
        help()
    elif len(sys.argv) > 4:
        sys.exit("YiraBot: Too many arguments!")
    else:
        command = sys.argv[1].lower()
        try:
            argument = sys.argv[2]
        except IndexError:
            argument = None

        process_command(command, argument)


def process_command(command, argument):
    """
    Processes the given command with the provided argument.
    """
    if command == "session":
        crawl_protected_page()
    elif command in ["get-html", "check"]:
        process_url_command(command, argument)
    elif command == "crawl" or command == "crawl-content":
        process_crawl_command(command, argument)
    else:
        print("YiraBot: Unknown Command.")


def process_url_command(command, argument):
    """
    Processes commands that require a URL argument.
    """
    try:
        url = validate_url(argument)
        if command == "get-html":
            get_html(url)
        elif command == "check":
            seo_error_analysis(url)
    except Exception as e:
        sys.exit(f"YiraBot: Error Occured: {e}")


def process_crawl_command(command, argument):
    """
    Processes crawl commands with an optional flag.
    """
    try:
        url = validate_url(argument)
        flag = sys.argv[3] if len(sys.argv) > 3 else None

        if flag not in ["-file", "-json", None]:
            sys.exit(f"YiraBot: Unrecognized Flag: {flag}")

        if command == "crawl":
            crawl(url, extract=(flag == "-file"), extract_json=(flag == "-json"))
        elif command == "crawl-content":
            crawl_content(url, extract=(flag == "-file"), extract_json=(flag == "-json"))

    except UnboundLocalError:
        sys.exit("YiraBot: Enter a link to crawl.")


def validate_url(url):
    """
    Validates and formats the URL if necessary.
    """
    if url.startswith("https://") or url.startswith("http://"):
        return url
    else:
        return "https://" + url


if __name__ == '__main__':
    main()
