# YiraBot
![Yira Logo](https://yira.me/static/images/favicon.ico "Yira") 

[![dependency - YiraBot](https://img.shields.io/badge/v1.0.6-PyPI-purple?logo=python&logoColor=white)](https://pypi.org/project/YiraBot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/OwenOrcan/YiraBot-Crawler/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/OwenOrcan/YiraBot-Crawler.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/yourusername/yourrepositoryname/stargazers/)
[![GitHub forks](https://img.shields.io/github/forks/OwenOrcan/YiraBot-Crawler.svg?style=social&label=Fork&maxAge=2592000)](https://GitHub.com/OwenOrcan/YiraBot-Crawler/network/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/OwenOrcan/YiraBot-Crawler.svg)](https://GitHub.com/OwenOrcan/YiraBot-Crawler/pull/)
[![GitHub release](https://img.shields.io/github/release/OwenOrcan/YiraBot-Crawler.svg)](https://GitHub.com/OwenOrcan/YiraBot-Crawler/releases/)
[![Custom Badge](https://img.shields.io/badge/Visit-Yira.me-red)](https://yira.me)




YiraBot is a sophisticated Python-based command-line tool, designed for users ranging from developers to data enthusiasts who require an efficient and user-friendly way to collect data from the web. This tool streamlines the process of web crawling, offering an intuitive interface and powerful capabilities to gather and organize web data with ease.


### Key Features:
**Web Crawling Made Simple:** With YiraBot, extracting information from web pages is straightforward. Whether it's for research, data analysis, or monitoring purposes, YiraBot efficiently navigates web content to retrieve the data you need.

**User-Friendly Setup and Uninstallation:** Getting started with YiraBot is a breeze. The program offers hassle-free installation and uninstallation processes, making it accessible for users of all technical levels.

**Command-Line Interface:** YiraBot leverages a command-line interface, allowing users to execute various tasks through simple yet powerful commands, such as setup, help, uninstall, and crawl.

**Ethical Crawling Practices:** Committed to ethical web scraping, YiraBot respects website's robots.txt policies, ensuring compliance and responsible data collection.

**Rich Data Extraction:** From extracting meta tags, images, and links to parsing sitemaps, YiraBot provides detailed insights about web pages, enhancing your data collection and analysis capabilities.

**Extracting Data To Files:** Feature to extract the data to a file.

**Cross-Platform Compatibility:** Compatible with every Operating System
### Ideal for Use Cases Such as:
-Academic research requiring data collection from multiple web sources.

-SEO analysis and website audits for meta tags, links, and content review.

-Monitoring websites for changes or updates.

-Gathering data for machine learning models or data analysis projects.


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
Displatying the help menu
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
