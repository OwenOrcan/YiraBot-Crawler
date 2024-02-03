from yirabot import Crawler

bot = Crawler()

github_data = bot.crawl("https://github.com")

print(github_data)
