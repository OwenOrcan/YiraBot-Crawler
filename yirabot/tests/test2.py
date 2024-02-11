from yirabot import Crawler

bot = Crawler()

data = bot.validate_routes("https://yira.me/static/sitemap.xml")

print(data)