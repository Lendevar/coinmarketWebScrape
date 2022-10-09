from bs4 import element
from bs4.element import PageElement
import requests
from bs4 import BeautifulSoup as bs
from requests.api import head
import re
import lxml
import selenium

from selenium import webdriver

import threading
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from datetime import datetime

nowCurrencies = {}
pastCurrencies = {}

pagesCount = 40
pastCount = 22

driverNow = webdriver.Chrome(executable_path="chromedriver.exe")
driverPast = webdriver.Chrome(executable_path="chromedriver.exe")

def scroll(definition, currentDriver):
    for i in range(1, definition+1):
        height = i/definition
        currentScript = "window.scrollTo(document.body.scrollHeight,document.body.scrollHeight*" + str(height) + ")"

        currentDriver.execute_script(currentScript)
        time.sleep(0.01)

def scrollToEnd(currentDriver):
    currentScript = "document.body.scrollHeight= 90"
    currentDriver.execute_script(currentScript)
    time.sleep(0.1)

    for i in range(1, 11):
        currentScript = "window.scrollTo(90,document.body.scrollHeight*" + str(0.9+i) + ")"
        currentDriver.execute_script(currentScript)
        time.sleep(0.1)

    time.sleep(0.1)


def collectNowData():
    for pageN in range(1, pagesCount+1):
        url ='https://coinmarketcap.com/?page=' + str(pageN)
        driverNow.get(url)

        scroll(100, driverNow)

        html = driverNow.page_source

        soup = bs(html, 'lxml')

        tableBody = soup.find("tbody")
        rows = tableBody.find_all("tr")

        for row in rows:
            cells = row.find_all("td")
            nowCurrencies.update({cells[2].find("p").text: int(cells[1].text)})

    return

def collectPastData():
    url = "https://coinmarketcap.com/historical/20211114/"
    driverPast.get(url)

    driverPast.set_window_position(1024, 1, windowHandle='current')


    for pageN in range(1, pastCount+1):
        scrollToEnd(driverPast)
        continue_link = driverPast.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/div/div[1]/div[3]/div[2]/button').click()

    scroll(500, driverPast)

    html = driverPast.page_source

    soup = bs(html, 'lxml')

    tableBody = soup.find("tbody")
    rows = tableBody.find_all("tr")

    for row in rows:
        cells = row.find_all("td")
        pastCurrencies.update({cells[1].find("a", {"class":"cmc-table__column-name--name cmc-link"}).text: int(cells[0].text)})

    return

tNow = threading.Thread(target=collectNowData, args=[])
tNow.start()

tPast = threading.Thread(target=collectPastData, args=[])
tPast.start()

tNow.join()
tPast.join()

myKeys = nowCurrencies.keys()

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

now = datetime.now()
dt_string = now.strftime("%H%M%S")

f= open(str(dt_string) + ".txt","w+", encoding='utf-8')

for item in sortedResult:
    print(item, " ", result.get(item))
    if result.get(item, None) != None:
        f.write(str(item) +  " " + str(result.get(item, None)) + "\r\n")

f.close()


