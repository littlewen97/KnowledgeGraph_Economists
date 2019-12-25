import Spider
import csv
from bs4 import BeautifulSoup
spider = Spider.Spider()
rows = []
for line in open('url.txt','r'):
    rows.append(line.rstrip('\n'))
for row in rows:
    soup = spider.getSoup(row)
    items = spider.getContent(soup)
    spider.createPersonCSV(items)
# soup = spider.getSoup('https://baike.baidu.com/item/%EF%BB%BF%E8%94%A1%E6%98%89/1020848')
# items = spider.getContent(soup)
# spider.printContent(items)