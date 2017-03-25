import time
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv

csvfile = open("met_exhibits.csv", 'w', newline='', encoding='utf-8')
c = csv.writer(csvfile)
# write the header row for CSV file
c.writerow(['titles', 'dates', 'links'])

driver = webdriver.Chrome('/Users/carolinejinks/Documents/python/scraping/chromedriver')  # Optional argument, if not specified will search path.
driver.get('http://www.metmuseum.org/exhibitions/current-exhibitions');

html = driver.page_source

bsObj = BeautifulSoup(html, "html.parser")

titles = []
dates = []
links = []

title_list = bsObj.findAll("h2", {"class":"card__title"})
for title in title_list:
    titles.append(title.get_text())

date_list = bsObj.findAll("strong")
for date in date_list:
    dates.append(date.get_text())

partial = []

for link in bsObj.findAll("a", href=re.compile("^(/exhibitions/listings/)((?!:).)*$")):
    if 'href' in link.attrs:
        partial.append(link.attrs['href'])


for part in partial:
    new_link = "http://www.metmuseum.org" + part
    links.append(new_link)
    
n = 0
for title in titles:

    c.writerow( [titles[n], dates[n], links[n]] )
    n = n + 1


csvfile.close()
driver.quit()
