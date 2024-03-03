from getpass import getpass
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from .data_extraction_functions import *
from .display_functions import *
from .helper_functions import *
from .saving_functions import *
from .seo_functions import *


# ============================================================
# CRAWLING AND ANALYSIS FUNCTIONS
# Core functions for crawling web pages and specific analyses.
# ============================================================


def crawl(url, extract=False, extract_json=False, session=None, mobile=False):
    """
    Crawls a given URL, extracting various information like metadata, links, and images,
    and optionally saves the data to a file in text or JSON format.

    Args:
        url (str): The URL to be crawled.
        extract (bool): If True, saves extracted data in text format. Defaults to False.
        extract_json (bool): If True, saves extracted data in JSON format. Defaults to False.
        session (Session, optional): A session object for authenticated requests.
        mobile (bool): If True, uses a mobile user agent for the request.

    Returns:
        None: Outputs to the console or files, based on parameters.
    """
    # Set user agent based on the 'mobile' flag
    headers = {'User-Agent': get_random_user_agent(mobile=mobile)}

    try:
        # Check if crawling is allowed by robots.txt
        if not is_allowed_by_robots_txt(url):
            print("YiraBot: Crawling forbidden by robots.txt")
            return

        # Make the request using a session if provided, else use requests.get
        response = session.get(url, headers=headers) if session else requests.get(url, headers=headers, timeout=10)

        # Handle server-induced delays
        dynamic_delay(response)

        print("YiraBot: Using Mobile User Agent") if mobile else None
        time.sleep(1) if mobile else None

        # Raise an exception for bad responses
        response.raise_for_status()

        # Parse the response content with BeautifulSoup
        soup = BeautifulSoup(response.text, features="html5lib")

        # Extract data from the parsed HTML
        data = extract_crawl_data(soup, url)

        # Save or display the extracted data
        if extract or extract_json:
            save_crawl_data(data, url, extract, extract_json)
        else:
            display_crawl_data(data)

    except (HTTPError, ConnectionError, Timeout, RequestException) as e:
        print(f"YiraBot: Error occurred: {e}")
    except Exception as e:
        print(f"YiraBot: An unexpected error occurred: {e}")


def crawl_content(url, extract=False, extract_json=False, session=None, mobile=False):
    """
    Crawls a URL specifically for its main content, such as paragraphs, headings, and lists,
    and optionally saves the data in text or JSON format.

    Args:
        url (str): The URL to be crawled for content.
        extract (bool): If True, saves extracted data in text format. Defaults to False.
        extract_json (bool): If True, saves extracted data in JSON format. Defaults to False.
        session (requests.Session, optional): A session object for authenticated requests.

    Returns:
        None: Outputs to the console or files, based on parameters.
    """
    headers = {'User-Agent': get_random_user_agent(mobile=mobile)}

    try:
        # Check if the URL is allowed by robots.txt
        if not is_allowed_by_robots_txt(url):
            print("YiraBot: Crawling forbidden by robots.txt")
            return

        # Perform the request with the provided session or a new session
        response = session.get(url, headers=headers, timeout=10) if session else requests.get(url, headers=headers, timeout=10)

        # Handle server-induced delays
        dynamic_delay(response)

        print("YiraBot: Using Mobile User Agent") if mobile else None
        time.sleep(1) if mobile else None

        # Check for successful response
        response.raise_for_status()

        # Parse the response content
        soup = BeautifulSoup(response.text, features="html5lib")

        # Extract content data from the parsed HTML
        data = extract_content_data(soup)

        # Decide whether to save or display the extracted data
        if extract or extract_json:
            save_crawl_data(data, url, extract, extract_json)
        else:
            display_crawl_data(data)

    except (HTTPError, ConnectionError, Timeout, RequestException) as e:
        print(f"YiraBot: Error occurred: {e}")
    except Exception as e:
        print(f"YiraBot: An unexpected error occurred: {e}")


def crawl_protected_page():
    """
    Handles the crawling of protected web pages by facilitating user authentication
    and offering a choice of crawling methods for protected content.
    """
    try:
        session = requests.Session()
        print("YiraBot: Session Started.")

        def login():
            """
            Prompts the user for login details and constructs the credentials payload.
            """
            login_url = input("Enter the login page URL: ").strip()
            if not login_url.startswith("https://"):
                sys.exit("YiraBot: Secure HTTPS connection required for login.")

            expected_response = input("Enter the success redirect URL: ").strip()
            if not expected_response.startswith("https://"):
                expected_response = "https://" + expected_response

            credentials = {
                input("Enter the username form input name: ").strip(): input("Enter your username: ").strip(),
                input("Enter the password form input name: ").strip(): getpass("Enter your password: ").strip()
            }

            return login_url, expected_response, credentials

        login_url, expected_response, credentials = login()
        response = session.post(login_url, data=credentials, timeout=10)
        response.raise_for_status()

        if not login_successful(response, expected_response):
            print("Login failed, please check your credentials.")
            return

        print(f"YiraBot: Successfully logged into {extract_domain(login_url)}")

        while True:
            protected_url = input("Enter the URL of the protected page: ").strip()
            if not protected_url.startswith("https://"):
                print("YiraBot: Secure HTTPS connection required.")
                continue

            crawl_choice = input("Select Crawl Method:\n1: Crawl\n2: Scrape\n3: SEO\nInput: ")
            try:
                crawl_choice = int(crawl_choice)
                if crawl_choice == 1:
                    crawl(protected_url, session=session)
                elif crawl_choice == 2:
                    crawl_content(protected_url, session=session)
                elif crawl_choice == 3:
                    seo_error_analysis(protected_url, session=session)
                else:
                    print("YiraBot: Invalid input, please enter a number from the choices.")
            except ValueError:
                print("YiraBot: Please enter a valid number for the crawl choice.")
    except KeyboardInterrupt:
        print("\nYiraBot: Session Stopped")


def get_html(url):
    """
    Downloads the complete HTML content of the specified URL and saves it as an HTML file.

    Args:
        url (str): The URL of the webpage to download.

    Returns:
        None: The function saves the HTML content to a file and outputs the file name.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Ensure the request was successful
        html = response.text

        # Create a safe filename from the URL and current timestamp
        safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"{safe_url}.{timestamp}.html"

        # Use the write_to_file function, assuming it supports HTML content
        write_to_file(html, filename, html=True)

        print(f"YiraBot: HTML file '{filename}' created.")

    except requests.exceptions.HTTPError as e:
        print(f"YiraBot Error: HTTP error occurred while trying to get HTML. {e}")
    except requests.exceptions.ConnectionError:
        print("YiraBot Error: Connection error occurred while trying to get HTML.")
    except requests.exceptions.Timeout:
        print("YiraBot Error: Timeout occurred while trying to get HTML.")
    except requests.exceptions.RequestException as e:
        print(f"YiraBot Error: An error occurred while trying to get HTML. {e}")
    except Exception as e:
        print(f"YiraBot Error: An unexpected error occurred. {e}")
