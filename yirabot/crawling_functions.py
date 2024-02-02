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


def crawl(url, extract=False, extract_json=False, session=None):
    """
    Crawls a given URL and extracts various information such as metadata, links, and images.
    Parameters:
    url (str): The URL to be crawled.
    extract (bool): If True, extracts data to a file. Defaults to False.
    extract_json (bool): If True, extracts data to a JSON file. Defaults to False.
    session (Session, optional): Requests session for authenticated crawling.
    Returns:
    None
    """
    headers = {'User-Agent': get_random_user_agent()}
    try:
        if not is_allowed_by_robots_txt(url):
            print("YiraBot: Crawling forbidden by robots.txt")
            return

        response = session.get(url, headers=headers) if session else requests.get(url, headers=headers)
        dynamic_delay(response)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, features="html5lib")
        data = extract_crawl_data(soup, url)

        if extract or extract_json:
            save_crawl_data(data, url, extract, extract_json)
            return

        display_crawl_data(data)
    except HTTPError as e:
        print(f"YiraBot: HTTP error occurred: {e}")
    except ConnectionError:
        print("YiraBot: Connection error occurred")
    except Timeout:
        print("YiraBot: Timeout error occurred")
    except RequestException:
        print("YiraBot: An error occurred during the request")
    except Exception as e:
        print(f"YiraBot: An unexpected error occurred: {e}")


def crawl_content(url, extract=False, extract_json=False, session=None):
    """
    Specifically crawls a URL for its main content like paragraphs, headings, and lists.
    Parameters:
    url (str): The URL to be crawled for content.
    extract (bool): If True, extracts data to a file. Defaults to False.
    extract_json (bool): If True, extracts data to a JSON file. Defaults to False.
    session (Session, optional): Requests session for authenticated crawling.
    Returns:
    None
    """
    headers = {'User-Agent': get_random_user_agent()}
    try:
        if not is_allowed_by_robots_txt(url):
            print("YiraBot: Crawling forbidden by robots.txt")
            return

        response = session.get(url, headers=headers) if session else requests.get(url, headers=headers)
        dynamic_delay(response)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, features="html5lib")
        data = extract_content_data(soup)

        if extract or extract_json:
            save_crawl_data(data, url, extract, extract_json)
            return

        display_crawl_data(data)
    except HTTPError as e:
        print(f"YiraBot: HTTP error occurred: {e}")
    except ConnectionError:
        print("YiraBot: Connection error occurred")
    except Timeout:
        print("YiraBot: Timeout error occurred")
    except RequestException:
        print("YiraBot: An error occurred during the request")
    except Exception as e:
        print(f"YiraBot: An unexpected error occurred: {e}")


def crawl_protected_page():
    """
    Handles the crawling of protected web pages that require authentication.
    """
    try:
        session = requests.Session()
        print("YiraBot: Session Started.")

        # Function to handle the login process
        def login():
            login_url = input("Enter the login page URL: ")
            if login_url.startswith("http://"):
                sys.exit(f"YiraBot: Cannot use authentication on HTTP websites, Not Secure.")
            if not login_url.startswith("https://"):
                login_url = "https://" + login_url

            expected_response = input("Enter the success redirect URL: ")
            if "/" not in expected_response:
                expected_response += "/"
            if not expected_response.startswith("https://"):
                expected_response = "https://" + expected_response

            username_field = input("Enter the username form input name: ")
            password_field = input("Enter the password form input name: ")
            username = input("Enter your username: ")
            password = getpass("Enter your password: ")

            return login_url, expected_response, {
                username_field: username,
                password_field: password
            }
    except KeyboardInterrupt:
        sys.exit("\nYiraBot: Session Stopped")


    # Attempt to log in
    try:
        login_url, expected_response, credentials = login()
        response = session.post(login_url, data=credentials)
        response.raise_for_status()
    except HTTPError as e:
        print(f"Login failed, HTTP error: {e}")
        return
    except ConnectionError:
        print("Login failed, connection error.")
        return
    except Timeout:
        print("Login failed, timeout error.")
        return
    except RequestException:
        print("Login failed, request error.")
        return
    except KeyboardInterrupt:
        print("\nYiraBot: Session Stopped")
        return


    # Check if login was successful
    if not login_successful(response, expected_response):
        print("Login failed, please check your credentials.")
        return

    print(f"YiraBot: Successfully logged into {extract_domain(login_url)}")
    print("YiraBot: Use CTRL-C to stop session.")

    # Crawling loop for protected pages
    while True:
        try:
            protected_url = input("Enter the URL of the protected page: ")
            if protected_url.startswith("http://"):
                print(f"YiraBot: Cannot use authentication on HTTP websites, Not Secure.")
                continue
            if not protected_url.startswith("https://"):
                protected_url = "https://" + protected_url

            crawl_choice = input("- Select Crawl Method:\n1:  Crawl\n2: Scrape\n3: SEO\nInput: ")
            crawl_choice = int(crawl_choice)
            if crawl_choice == 1:
                crawl(protected_url, session=session)
            elif crawl_choice == 2:
                crawl_content(protected_url, session=session)
            elif crawl_choice == 3:
                seo_error_analysis(protected_url, session=session)
            else:
                print("YiraBot: Unexpected Input.")
        except ValueError:
            print("YiraBot: Please enter a valid number for crawl choice.")
        except KeyboardInterrupt:
            print("\nYiraBot: Session Stopped")
            break


def get_html(url):
    """
    Downloads the complete HTML of the specified URL and saves it as a file.
    Parameters:
    url (str): URL of the webpage to download.
    """
    try:
        response = requests.get(url)
        html = response.text
        safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"{safe_url}.{timestamp}.html"

        write_to_file(html, filename, html=True)

        print(f"YiraBot: HTML file '{filename}' created.")
    except Exception as e:
        print(f"YiraBot Error: An error occurred while trying to get HTML. {e}")
