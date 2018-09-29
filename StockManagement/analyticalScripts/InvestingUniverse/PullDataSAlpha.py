import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import bs4 as bs

#https://free-proxy-list.net/

def setDriverUp():
    chrome_options = webdriver.ChromeOptions()
   # chrome_options.add_argument('--proxy-server=%s' % IP)
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery");
    chrome_options.add_argument("--start-maximized")
   # chrome_options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver
    

def StockInfoGrab(StockTicker, driver):
         
    url = "https://seekingalpha.com/symbol/"+ StockTicker + "/overview"
    response = driver.get(url)
    
    YearandNumbOfWorkers = {}
    
    if driver.title == 'Sorry, the page you are looking for was not found | Seeking Alpha':
        return 2000
    
    else:
        feature = {
            "IPODate": "//tr[@title='The year the company was founded']/td[2]",
            "Employees": "//tr[@title='Represents the number of both full- and part-time employees of the company']/td[2]",
        }

        try:
            YearandNumbOfWorkers["IPODate"] = driver.find_element_by_xpath(feature["IPODate"]).text
            YearandNumbOfWorkers["Employees"] = driver.find_element_by_xpath(feature["Employees"]).text
            return YearandNumbOfWorkers
        except:
            print("Failed to gather data for" + StockTicker)

        


