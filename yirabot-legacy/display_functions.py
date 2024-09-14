import textwrap
from rich.console import Console
from rich.table import Table


def display_crawl_data(data):
    """
    Displays the crawled data in a structured table format using Rich library.

    Parameters:
    - data (dict): The data to be displayed, expected to be a dictionary with keys
                   representing data categories and values being the corresponding data.

    Returns:
    - None: This function outputs to the console and returns nothing.
    """
    console = Console()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Key", style="dim", width=22)
    table.add_column("Value", overflow="fold")

    # Add data to the table, wrapping text for the 'Value' column
    for key, value in data.items():
        value_str = ', '.join(value) if isinstance(value, list) else str(value)
        table.add_row(key.capitalize(), textwrap.fill(value_str, width=80))
    console.print(table)


def display_seo_results(title_length, title_status, meta_desc_length, meta_desc_status, keyword_results, headings,
                        heading_structure_status, images_without_alt, is_responsive, responsiveness_message,
                        social_media_integration, website_language):
    """
    Displays the results of an SEO analysis in a structured table format. Each aspect of the analysis
    is represented as a row in the table, detailing the SEO performance and recommendations.

    Parameters:
    - title_length (int): Length of the title tag.
    - title_status (str): Status of the title tag (e.g., "Good", "Too Short", "Too Long").
    - meta_desc_length (int): Length of the meta description.
    - meta_desc_status (str): Status of the meta description (e.g., "Good", "Too Short", "Too Long").
    - keyword_results (dict): A dictionary of top keywords and their occurrences.
    - headings (dict): A dictionary of heading tags (e.g., H1, H2) and their count.
    - heading_structure_status (str): Status of the heading structure (e.g., "Good", "Improvable").
    - images_without_alt (list): List of images without alt text.
    - is_responsive (bool): Indicates if the website is mobile responsive.
    - responsiveness_message (str): Descriptive message about the website's responsiveness.
    - social_media_integration (dict): A dictionary indicating the presence of social media integration.
    - website_language (str): Language of the website.

    Returns:
    - None: Outputs to the console.
    """
    console = Console()
    table = Table(title="SEO Analysis Results", show_header=True, header_style="bold blue")

    table.add_column("Aspect", style="dim", width=20)
    table.add_column("Details/Length", justify="right")
    table.add_column("Status/Value", overflow="fold")

    table.add_row("Title Tag", str(title_length), title_status)
    table.add_row("Meta Description", str(meta_desc_length), meta_desc_status)

    keywords_display = ', '.join([f"{word} ({count})" for word, count in keyword_results])
    table.add_row("Top Keywords", "N/A", keywords_display)

    headings_display = ', '.join([f"{tag}: {count}" for tag, count in headings.items()])
    table.add_row("Headings", "N/A", headings_display if headings else "No Headers")

    no_alt_display = ', '.join(images_without_alt) if images_without_alt else "All images have alt text"
    table.add_row("Images without Alt Text", str(len(images_without_alt)), no_alt_display)

    table.add_row("Mobile Responsiveness", "N/A", responsiveness_message)

    social_media_str = ", ".join([platform for platform, integrated in social_media_integration.items() if integrated])
    social_media_str = social_media_str if social_media_str else "No Social Media Integration Detected"
    table.add_row("Social Media Integration", "N/A", social_media_str)

    table.add_row("Website Language", "N/A", website_language)

    console.print(table)
