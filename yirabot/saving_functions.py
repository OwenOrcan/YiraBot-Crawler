from datetime import datetime
from rich import print
from .helper_functions import write_to_file

# ============================================================
# SAVING DATA FUNCTIONS
# Functions that handle saving the crawled data.
# ============================================================

def save_crawl_data(data, url, extract, extract_json):
    """
    Saves the crawled data to a file in text or JSON format.
    Parameters:
    data (dict): The data to be saved.
    url (str): The URL of the crawled site.
    extract (bool): Whether to save data in text format.
    extract_json (bool): Whether to save data in JSON format.
    Returns:
    None
    """
    safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"{safe_url}.{timestamp}"

    if extract:
        write_to_file(data, f"{filename}.txt")
        print("YiraBot: Text file created.")
    if extract_json:
        write_to_file(data, f"{filename}.json", jsonify=True)
        print("YiraBot: JSON file created.")
