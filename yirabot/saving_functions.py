from datetime import datetime
from rich import print
from .helper_functions import write_to_file


def save_crawl_data(data, url, extract, extract_json):
    """
    Saves the crawled data to files in specified formats based on the parameters.
    The filename is derived from the URL and the current timestamp.

    Args:
        data (dict): The data to be saved, expected to be a dictionary.
        url (str): The URL of the crawled site, used to generate part of the filename.
        extract (bool): If True, saves the data in text format.
        extract_json (bool): If True, saves the data in JSON format.

    Returns:
        None: The function outputs files and does not return any value.
    """
    # Sanitize the URL to create a safe filename
    safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"{safe_url}.{timestamp}"

    # Save data in text format
    if extract:
        write_to_file(data, f"{filename}.txt")
        print("YiraBot: Text file created.")

    # Save data in JSON format
    if extract_json:
        write_to_file(data, f"{filename}.json", jsonify=True)
        print("YiraBot: JSON file created.")