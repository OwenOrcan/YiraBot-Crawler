import textwrap
import time
from rich.console import Console
from rich.table import Table
from tqdm import tqdm


# ============================================================
# DISPLAY FUNCTIONS
# Functions for displaying data.
# ============================================================

def display_crawl_data(data):
    """
    Displays the crawled data in a tabular format using the Rich library.
    Parameters:
    data (dict): The data to be displayed.
    Returns:
    None
    """
    console = Console()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Key", style="dim", width=22)
    table.add_column("Value", overflow="fold")

    for key, value in data.items():
        if isinstance(value, list):
            value = ', '.join(value)
        table.add_row(key.capitalize(), textwrap.fill(str(value), width=80))
    console.print(table)

def display_seo_analysis_results(images_without_alt, broken_links, url):
    """
    Displays the results of the SEO analysis in a tabular format.
    Parameters:
    images_without_alt (list): List of images without alt attributes.
    broken_links (list): List of broken internal links.
    url (str): URL of the analyzed webpage.
    """
    with tqdm(total=100, desc=f'Yirabot SEO Analysis: {url}') as pbar:
        for _ in range(100):
            time.sleep(0.01)
            pbar.update(1)

    console = Console()
    table = Table(title="SEO Analysis Results", show_header=True, header_style="bold blue")
    table.add_column("Type", style="dim", width=15)
    table.add_column("Count", justify="right")
    table.add_column("Details", overflow="fold")

    table.add_row("Images w/o Alt", str(len(images_without_alt)),
                  "\n".join(img['src'] for img in images_without_alt[:5]))
    table.add_row("Broken Links", str(len(broken_links)),
                  "\n".join(broken_links[:5]))

    console.print(table)
