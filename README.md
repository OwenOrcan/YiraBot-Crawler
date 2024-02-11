
![YiraBot ](https://github.com/OwenOrcan/YiraBot-Crawler/assets/144565916/54cfd22f-9bc8-4505-b3fe-ad6dd0de83d4)

# [📰 Read the Latest Release Notes](https://github.com/OwenOrcan/YiraBot-Crawler/releases)


### Development Status on [YiraBot 1.0.9](https://github.com/OwenOrcan/YiraBot-Crawler/blob/python-module-development/1.0.9.md)

| Feature | Status | Progress |
| ------- | ------ | -------- |
| Crawler class and methods | Completed | ▮▮▮▮▮▮▮▮▮▮ (100%) |
| New Feature to validate routes | Completed | ▮▮▮▮▮▮▮▮▮▮ (100%) |
| SEO class and methods | Not Started | ▯▯▯▯▯▯▯▯▯▯ (0%) |
| General crawling and scraping functions | Not Started | ▯▯▯▯▯▯▯▯▯▯ (0%) |
| Minor fixes and additions| Not Started| ▯▯▯▯▯▯▯▯▯▯ (0%) |



<a href="https://www.buymeacoffee.com/owenorcan" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 29px !important;width: 130px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
[![PyPI - Version](https://img.shields.io/pypi/v/YiraBot?style=for-the-badge&logo=PyPI)](https://pypi.org/project/YiraBot/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/YiraBot?style=for-the-badge)](https://pypistats.org/packages/yirabot)
[![GitHub Repo stars](https://img.shields.io/github/stars/OwenOrcan/YiraBot-Crawler?style=for-the-badge&logo=github&color=pink)](https://github.com/OwenOrcan/YiraBot-Crawler/stargazers)


## Overview
YiraBot isn't just another web scraping tool; it's about making web crawling simple and accessible for everyone. Whether you're a seasoned developer, a data enthusiast, or just dabbling in Python, YiraBot is designed to make your life easier. With its user-friendly command-line interface and Python module flexibility, YiraBot streamlines the process of extracting data from the web, making it a straightforward and enjoyable experience.

## Key Features

### Command-Line Simplicity
- **Easy-to-Use Commands:** Experience the ease of web crawling with intuitive and powerful commands.
- **Versatility for All Tasks:** Whether it's a quick data extraction or a more complex scraping job, YiraBot is up to the task, all from the command line.
### Module Integration
- **Enhanced Scripting Flexibility:** Not just a command-line tool, YiraBot also integrates seamlessly into your Python scripts, expanding your data scraping capabilities.
### Ethical and Efficient Crawling
- **Adherence to Web Standards:** YiraBot respects the rules of the web by complying with robots.txt policies.
- **Comprehensive Data Extraction:** From meta tags to images and links, YiraBot is thorough, ensuring you get all the data you need.
### User Friendly Experience
- **Hassle-Free Data Export:** Exporting your data is a breeze with YiraBot's straightforward options.
- **Cross-Platform Compatibility:** YiraBot works smoothly whether you're on Linux, Windows, or macOS.



## Ideal Uses
- **Academic Research:** Effortlessly gather data from various web sources.
- **SEO and Website Analysis:** Conduct comprehensive reviews of website content and SEO elements.
- **Website Monitoring:** Stay updated with changes and updates on web pages.
- **Machine Learning Data Collection:** Easily collect data for machine learning models and analysis.

## Getting Started

Ensure Python and Pip are on your system, then simply run:
```bash
pip install YiraBot
```
### Command-Line Usage
Display the help menu:
```bash
yirabot
```
Explore Yirabot's Capabilities:

- **Crawl:** yirabot crawl example.com (-file or -json to extract data)
- **Scrape:** yirabot scrape example.com (-file or -json to extract data)
- **Advanced SEO Analysis** yirabot seo example.com
- **Clone a webpage:** yirabot get-html example.com
- **Start a Session to use commands on authentication protected pages:** yirabot session
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

## Contributions

Contributions to the YiraBot project are welcomed. Feel free to fork the repository, make your changes, and submit pull requests.

All contributors must follow the [Contribution Policy](https://github.com/OwenOrcan/YiraBot-Crawler/blob/master/CONTRIBUTING.md) to ensure a smooth and collaborative development process.

### License
YiraBot is open-sourced software licensed under the [MIT LICENSE](https://github.com/OwenOrcan/YiraBot-Crawler?tab=MIT-1-ov-file).

## Developers:

<table>
  <tr>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/144565916?v=4" alt="Owen Orcan" width="100" height="100"/><br>
      <a href="https://github.com/OwenOrcan">Owen Orcan</a>
    </td>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/133255559?v=4" alt="Yigit Ocak" width="100" height="100"/><br>
      <a href="https://github.com/YigitOcak">Yigit Ocak</a>
    </td>
  </tr>
</table>
