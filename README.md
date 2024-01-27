![YiraBot](https://github.com/OwenOrcan/YiraBot-Crawler/assets/144565916/54cfd22f-9bc8-4505-b3fe-ad6dd0de83d4)

<a href="https://www.buymeacoffee.com/owenorcan" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;"></a>
[![dependency - YiraBot](https://img.shields.io/badge/v1.0.7.1-PyPI-purple?logo=python&logoColor=white)](https://pypi.org/project/YiraBot)
[![GitHub stars](https://img.shields.io/github/stars/OwenOrcan/yirabot-crawler.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/OwenOrcan/YiraBot-Crawler/stargazers/)

## Overview

Meet YiraBot – your new web crawling and SEO analysis companion! Designed for simplicity and ease of use, YiraBot makes web scraping accessible to everyone. Whether you're a seasoned developer, a data enthusiast, or just exploring Python, YiraBot streamlines web data extraction, turning it into an effortless and satisfying task.

## Key Features

### Command-Line Simplicity
- **User-Friendly Commands:** Jump right into web crawling with straightforward and powerful commands.
- **Ready for Any Task:** From quick data grabs to intricate scraping jobs, YiraBot handles it all through the command line.

### Module Integration
- **Scripting Made Easy:** More than a command-line tool – YiraBot integrates flawlessly with your Python scripts for enhanced scraping capabilities.

### Ethical and Efficient Crawling
- **Respecting Web Standards:** YiraBot adheres to robots.txt policies, ensuring responsible web scraping.
- **Thorough Data Extraction:** Extract everything from meta tags to images and links – YiraBot doesn't miss a beat.

### User-Friendly Experience
- **Simple Data Export:** Exporting your data is straightforward with YiraBot's easy options.
- **Cross-Platform Performance:** Enjoy seamless operation across Linux, Windows, and macOS.

## Ideal Uses
- **Academic Research:** Gather web data effortlessly for your research projects.
- **SEO and Website Analysis:** Dive deep into website content and SEO elements for comprehensive insights.
- **Website Monitoring:** Keep tabs on changes and updates across web pages.
- **Machine Learning Data Gathering:** Conveniently collect data sets for machine learning purposes.

## Getting Started

First things first – make sure Python and Pip are installed on your system. Then, you're just one command away:
```bash
pip install YiraBot
```
### Command-Line Usage
Kick things off with the help menu:
```bash
yirabot
```
Dive into YiraBot's Capabilities:
- **Basic Crawl: 'yirabot crawl example.com'**
- **Save Crawl to a File: 'yirabot crawl example.com -file' (or -json)**
- **Content Crawl: 'yirabot crawl-content example.com'**
- **Check Website for Issues: 'yirabot check example.com'**
- **Clone a Webpage: 'yirabot get-html example.com'**
- **Crawl Authentication Protected Pages: 'yirabot session'**

# Using Yirabot in Your Projects
Easily integrate YiraBot in your scripts like so:
```python
from yirabot import Yirabot

# Create a YiraBot instance
bot = Yirabot()

# Example usage
html_content = bot.get_html('https://example.com')
print(html_content)
```
## Methods:
- **get_html(url):** Retrieves the HTML content of a webpage.
- **is_allowed_by_robots_txt(url):** Checks if a URL is permitted for crawling by robots.txt.
- **parse_sitemap(url):** Finds URLs by parsing a website's sitemap.
- **crawl(url):** Performs a comprehensive crawl of a URL.
- **crawl_content(url):** Extracts detailed content like text, headings, and lists.
## Examples
**Crawl a Webpage:**
```python
data = bot.crawl('https://example.com')
print(data)
```
**Extract Web Content:**
```python
content = bot.crawl_content('https://example.com')
print(content)
```
**Check Crawlability of a WebPage:**
```python
crawlable = bot.is_allowed_by_robots_txt('https://example.com')
print(crawlable)
```
**Discover URLs from a Website's Sitemap:**
```python
urls = bot.parse_sitemap("https://example.com")
print(urls)
```

### Contributing
Your contributions are what make YiraBot even better. Fork the repository, make your changes, and create a pull request to join in!
### License
iraBot is open-source and proudly bears the MIT LICENSE.