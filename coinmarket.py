from bs4.element import PageElement
import requests
from bs4 import BeautifulSoup as bs
from requests.api import head
import re
import lxml
import selenium

from selenium import webdriver
import time

nowCurrencies = {}
pastCurrencies = {}

#print("Number of pages to load")
#pagesCount = input()


pagesCount = 40
pastCount = 22

#chrome_options = webdriver.ChromeOptions()
#prefs = {"profile.managed_default_content_settings.images": 2}
#chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path="chromedriver.exe")

def scrollFast():
    for i in range(1, 100+1):
        height = i/100
        currentScript = "window.scrollTo(document.body.scrollHeight,document.body.scrollHeight*" + str(height) + ")"

        driver.execute_script(currentScript)
        time.sleep(0.01)

def scrollSlow():
    for i in range(1, 200+1):
        height = i/200

        currentScript = "window.scrollTo(document.body.scrollTop,document.body.scrollHeight*" + str(height) + ")"

        driver.execute_script(currentScript)
        #time.sleep(0.01)
    
    time.sleep(10)



for pageN in range(1, pagesCount+1):
    url ='https://coinmarketcap.com/?page=' + str(pageN)
    driver.get(url)

    scrollFast()

    html = driver.page_source

    soup = bs(html, 'lxml')

    tableBody = soup.find("tbody")
    rows = tableBody.find_all("tr")

    for row in rows:
        cells = row.find_all("td")
        nowCurrencies.update({cells[2].find("p").text: int(cells[1].text)})

        #print(cells[1].text, "=", cells[2].find("p").text)

url = "https://coinmarketcap.com/historical/20211107/"
driver.get(url)

for pastN in range(1, pastCount + 1):
    
    scrollSlow()
    continue_link = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/div/div[1]/div[3]/div[2]/button').click()


html = driver.page_source

soup = bs(html, 'lxml')

tableBody = soup.find("tbody")
rows = tableBody.find_all("tr")

for row in rows:
    cells = row.find_all("td")
    #print(cells[0].text, " ", cells[1].find("a", {"class":"cmc-table__column-name--name cmc-link"}).text)
    
    pastCurrencies.update({cells[1].find("a", {"class":"cmc-table__column-name--name cmc-link"}).text: int(cells[0].text)})

    #print(cells[1].text, "=", cells[2].find("p").text)

#print(nowCurrencies)
#print(pastCurrencies)

myKeys = nowCurrencies.keys()

#print(myKeys)

result = {}

for key in myKeys:
    nowRank = nowCurrencies.get(key, None)
    pastRank = pastCurrencies.get(key, None)

    if nowRank != None and pastRank != None:
        print(nowRank, " - " , pastRank, " = ",  nowRank - pastRank)
        difference = nowRank - pastRank

        #print(nowRank, " ", key, " ", difference)

        resKey = str(nowRank) + " " + str(key)

        result.update({resKey:difference})
    
    else:
        #print(key, " is not found in past/future")
        pass

sortedResult = sorted(result, key = result.get, reverse = False)

f= open("result.txt","w+")

for item in sortedResult:
    print(item, " ", result.get(item))
    if result.get(item, None) != None:
        f.write(str(item) +  " " + str(result.get(item, None)) + "\r\n")

f.close()



