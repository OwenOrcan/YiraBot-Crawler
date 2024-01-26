
![YiraBot ](https://github.com/OwenOrcan/YiraBot-Crawler/assets/144565916/54cfd22f-9bc8-4505-b3fe-ad6dd0de83d4)


[![dependency - YiraBot](https://img.shields.io/badge/v1.0.7-PyPI-purple?logo=python&logoColor=white)](https://pypi.org/project/YiraBot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/OwenOrcan/YiraBot-Crawler/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/OwenOrcan/yirabot-crawler.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/OwenOrcan/YiraBot-Crawler/stargazers/)
[![GitHub release](https://img.shields.io/github/release/OwenOrcan/YiraBot-Crawler.svg)](https://GitHub.com/OwenOrcan/YiraBot-Crawler/releases/)
[![Custom Badge](https://img.shields.io/badge/Visit-Yira.me-red)](https://yira.me)
<a href="https://www.buymeacoffee.com/owenorcan" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## Overview
YiraBot is a sophisticated tool designed for efficient web data collection. Primarily a powerful Python-based command-line tool, it also doubles as an integrable module for Python projects. Ideal for developers, data enthusiasts, and researchers, YiraBot streamlines web crawling with an intuitive interface and robust capabilities.

## Key Features

### Command-Line Focus
- **Intuitive Command-Line Interface**: Execute various tasks through simple yet powerful commands, making web crawling accessible and efficient.
- **Versatile Usage**: Ideal for quick tasks or complex data extraction processes, all manageable through the command line.

### Module Integration
- **Python Library Flexibility**: In addition to its command-line prowess, YiraBot can be imported and used as a Python module, offering extended functionality in Python scripts.

### Ethical and Efficient Crawling
- **Respect for Robots.txt**: Adheres to ethical scraping standards by complying with website's robots.txt policies.
- **Rich Data Extraction**: Capable of extracting meta tags, images, links, and parsing sitemaps for comprehensive web analysis.

### User Experience
- **Data Export Capabilities**: Features include the extraction of data to files for easy analysis and record-keeping.

### Cross-Platform Compatibility
- **Universal Application**: Works seamlessly across various operating systems.

## Ideal Use Cases
- **Academic Research**: Gathering data from diverse web sources for scholarly studies.
- **SEO and Website Audits**: Reviewing meta tags, links, and content for SEO analysis.
- **Website Monitoring**: Tracking updates or changes across web pages.
- **Data Gathering for Machine Learning and Analysis**: Collecting web data for machine learning models and data projects.

## Installation

Ensure Python and Pip is installed on your system before installing YiraBot. Follow these steps for installation:
```bash
pip install YiraBot
```
## Command-Line Usage
```bash
yirabot <command> [arguments]
```
### Examples
Displaying the help menu
```bash
yirabot
```
Crawling a webpage:
```bash
yirabot crawl example.com
```
Crawling a webpage and extracting the data to a file.
```bash
yirabot crawl example.com -file
```
Crawling a webpage to get the content:
```bash
yirabot crawl-content example.com
```
Crawling a webpage to get the content and extracting the data to a json file
```bash
yirabot crawl-content example.com -json
```
Checking a webpage for broken code and issues
```bash
yirabot check example.com
```
Making an exact copy of a webpage
```bash
yirabot get-html example.com
```
# Use YiraBot On Your Own Projects.

## Usage:
Import and use Yirabot in your python script as follows.
```python
from yirabot import Yirabot

# Create an instance of YiraBot
bot = Yirabot()

# Example usage
html_content = bot.get_html('https://example.com')
print(html_content)
```
## Methods:
- **get_html(url):** Retrieves the HTML content of a webpage.
- **is_allowed_by_robots_txt(url):** Checks if crawling a URL is allowed by robots.txt.
- **parse_sitemap(url):** Parses the sitemap of a website to find URLs.
- **crawl(url):** Crawls a URL and extracts various information.
- **crawl_content(url):** Extracts detailed content like paragraphs, headings, and lists.
## Examples
**Crawling a Webpage**
```python
data = bot.crawl('https://example.com')
print(data)
```
**Extracting Content**
```python
content = bot.crawl_content('https://example.com')
print(content)
```
**Checking if a WebPage is crawlable**
```python
crawlable = bot.is_allowed_by_robots_txt('https://example.com')
print(crawlable)
```
**Parse the sitemap of a Website to find URL's**
```python
urls = bot.parse_sitemap("https://example.com")
print(urls)
```

### Contributing
Contributions to the YiraBot project are welcomed. Feel free to fork the repository, make your changes, and submit pull requests.
### License
YiraBot is open-sourced software licensed under the [MIT LICENSE](https://github.com/OwenOrcan/YiraBot-Crawler?tab=MIT-1-ov-file).
