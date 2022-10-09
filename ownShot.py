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

driverNow = webdriver.Chrome(executable_path="chromedriver.exe")

def scroll(definition, currentDriver):
    for i in range(1, definition+1):
        height = i/definition
        currentScript = "window.scrollTo(document.body.scrollHeight,document.body.scrollHeight*" + str(height) + ")"

        currentDriver.execute_script(currentScript)
        time.sleep(0.01)

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

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%y-%H")

    f= open(str(dt_string) + ".txt","w+", encoding='utf-8')

    for item in nowCurrencies:
        #print(item, " ", nowCurrencies.get(item))
        if nowCurrencies.get(item, None) != None:
            f.write(str(item) +  "+-+" + str(nowCurrencies.get(item, None)) + "\r\n")

    return

tNow = threading.Thread(target=collectNowData, args=[])
tNow.start()

tNow.join()

pastFile = open('18-11-21-18.txt', "r", encoding='utf-8')
pastFileContent = pastFile.readlines()

for line in pastFileContent:
    if line != "\n":
        pastCurrencies.update({line.split("+-+")[0]:line.split("+-+")[1].removesuffix("\n")})

myKeys = nowCurrencies.keys()

result = {}

for key in myKeys:
    if nowCurrencies.get(key, None) != None and pastCurrencies.get(key, None):

        nowRank = int(nowCurrencies.get(key, None))
        pastRank = int(pastCurrencies.get(key, None))

        if nowRank != None and pastRank != None:
            print(nowRank, " - " , pastRank, " = ",  nowRank - pastRank)
            difference = nowRank - pastRank

            if difference != 0:

                resKey = str(nowRank) + " " + str(key)

                result.update({resKey:difference})

else:
    #print(key, " is not found in past/future")
    pass


sortedResult = sorted(result, key = result.get, reverse = False)

now = datetime.now()
dt_string = "LastComparement"

f= open(str(dt_string) + ".txt","w+", encoding='utf-8')

for item in sortedResult:
    print(item, " ", result.get(item))
    if result.get(item, None) != None:
        f.write(str(item) +  " " + str(result.get(item, None)) + "\r\n")

f.close()

