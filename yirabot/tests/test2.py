from yirabot import Yirabot

bot = Yirabot()

data1 = bot.crawl("https://yira.me")
data2 = bot.scrape("https://yira.me")
data3 = bot.validate("https://yira.me/static/sitemap.xml")
data4 = bot.seo_analysis("https://yira.me")

