from yirabot import Crawler

bot = Crawler()

routes = bot.validate_routes("https://yira.me/static/sitemap.xml")

data = bot.crawl("https://yira.me")

content = bot.scrape("https://yira.me")

print("Routes: ",routes)
print("Data: ", data)
print("Content: ",content)

