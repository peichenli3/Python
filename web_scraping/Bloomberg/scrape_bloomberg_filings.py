# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import os
import shutil
from xml.etree.ElementPath import xpath_tokenizer
import requests
import sys
from lxml import html
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


INPUT_FILE_PATH = "C://Users/Kevin/Desktop/Bloomberg_law/input.json"
DOWNLOAD_DIR_PATH = ""
CHROME_DRIVER_PATH = ""

courts = ["U.S. Bankruptcy Court For The Central District Of California",
          "U.S. Bankruptcy Court For The Northern District Of Illinois",
          "U.S. Bankruptcy Court For The Middle District Of Florida",
          "U.S. Bankruptcy Court For The Eastern District Of Michigan",
          "U.S. Bankruptcy Court For The Northern District Of Ohio",
          "U.S. Bankruptcy Court For The District Of New Jersey",
          "U.S. Bankruptcy Court For The Northern District Of Georgia",
          "U.S. Bankruptcy Court For The District Of Arizona",
          "U.S. Bankruptcy Court For The Southern District Of Ohio",
          "U.S. Bankruptcy Court For The Eastern District Of California",
          "U.S. Bankruptcy Court For The Southern District Of Florida",
          "U.S. Bankruptcy Court For The Southern District Of Indiana",
          "U.S. Bankruptcy Court For The District Of Maryland",
          "U.S. Bankruptcy Court For The Eastern District Of Virginia",
          "U.S. Bankruptcy Court For The Western District Of Washington",
          "U.S. Bankruptcy Court For The District Of Colorado",
          "U.S. Bankruptcy Court For The District Of Oregon",
          "U.S. Bankruptcy Court For The District Of Minnesota",
          "U.S. Bankruptcy Court For The District Of Massachusetts",
          "U.S. Bankruptcy Court For The Eastern District Of New York",
          "U.S. Bankruptcy Court For The Northern District Of California",
          "U.S. Bankruptcy Court For The Southern District Of California",
          "U.S. Bankruptcy Court For The Eastern District Of Wisconsin",
          "U.S. Bankruptcy Court For The Northern District Of Indiana",
          "U.S. Bankruptcy Court For The District Of Nevada",
          "U.S. Bankruptcy Court For The Western District Of Michigan",
          "U.S. Bankruptcy Court For The Northern District Of Alabama",
          "U.S. Bankruptcy Court For The Eastern District Of Missouri",
          "U.S. Bankruptcy Court For The Eastern District Of Tennessee",
          "U.S. Bankruptcy Court For The District Of Utah",
          "U.S. Bankruptcy Court For The Northern District Of New York",
          "U.S. Bankruptcy Court For The Eastern District Of Pennsylvania",
          "U.S. Bankruptcy Court For The Western District Of Missouri",
          "U.S. Bankruptcy Court For The Western District Of Pennsylvania",
          "U.S. Bankruptcy Court For The Western District Of Kentucky",
          "U.S. Bankruptcy Court For The District Of Connecticut",
          "U.S. Bankruptcy Court For The Eastern District Of Kentucky",
          "U.S. Bankruptcy Court For The Northern District Of Texas",
          "U.S. Bankruptcy Court For The Western District Of Oklahoma",
          "U.S. Bankruptcy Court For The Southern District Of Texas",
          "U.S. Bankruptcy Court For The Middle District Of Tennessee",
          "U.S. Bankruptcy Court For The Southern District Of New York",
          "U.S. Bankruptcy Court For The Western District Of New York",
          "U.S. Bankruptcy Court For The Western District Of Virginia",
          "U.S. Bankruptcy Court For The Middle District Of Pennsylvania",
          "U.S. Bankruptcy Court For The Western District Of Texas",
          "U.S. Bankruptcy Court For The District Of Kansas",
          "U.S. Bankruptcy Court For The Southern District Of Mississippi",
          "U.S. Bankruptcy Court For The Western District Of Wisconsin",
          "U.S. Bankruptcy Court For The Middle District Of Georgia",
          "U.S. Bankruptcy Court For The Western District Of Tennessee",
          "U.S. Bankruptcy Court For The Eastern District Of Washington",
          "U.S. Bankruptcy Court For The Eastern District Of Arkansas",
          "U.S. Bankruptcy Court For The District Of New Mexico",
          "U.S. Bankruptcy Court For The Western District Of Louisiana",
          "U.S. Bankruptcy Court For The District Of Idaho",
          "U.S. Bankruptcy Court For The District Of South Carolina",
          "U.S. Bankruptcy Court For The Southern District Of Iowa",
          "U.S. Bankruptcy Court For The District Of Nebraska",
          "U.S. Bankruptcy Court For The Eastern District Of North Carolina",
          "U.S. Bankruptcy Court For The Central District Of Illinois",
          "U.S. Bankruptcy Court For The Southern District Of Illinois",
          "U.S. Bankruptcy Court For The Northern District Of Oklahoma",
          "U.S. Bankruptcy Court For The Western District Of North Carolina",
          "U.S. Bankruptcy Court For The Eastern District Of Louisiana",
          "U.S. Bankruptcy Court For The Northern District Of Florida",
          "U.S. Bankruptcy Court For The Western District Of Arkansas",
          "U.S. Bankruptcy Court For The Eastern District Of Texas",
          "U.S. Bankruptcy Court For The District Of Rhode Island",
          "U.S. Bankruptcy Court For The Northern District Of Mississippi",
          "U.S. Bankruptcy Court For The Southern District Of West Virginia",
          "U.S. Bankruptcy Court For The District Of New Hampshire",
          "U.S. Bankruptcy Court For The Middle District Of North Carolina",
          "U.S. Bankruptcy Court For The Southern District Of Georgia",
          "U.S. Bankruptcy Court For The Northern District Of Iowa",
          "U.S. Bankruptcy Court For The Middle District Of Alabama",
          "U.S. Bankruptcy Court For The District Of Maine",
          "U.S. Bankruptcy Court For The Eastern District Of Oklahoma",
          "U.S. Bankruptcy Court For The District Of Hawaii",
          "U.S. Bankruptcy Court For The Northern District Of West Virginia",
          "U.S. Bankruptcy Court For The District Of Montana",
          "U.S. Bankruptcy Court For The Southern District Of Alabama",
          "U.S. Bankruptcy Court For The District Of Puerto Rico",
          "U.S. Bankruptcy Court For The District Of Delaware",
          "U.S. Bankruptcy Court For The District Of South Dakota",
          "U.S. Bankruptcy Court For The Middle District Of Louisiana",
          "U.S. Bankruptcy Court For The District Of Wyoming",
          "U.S. Bankruptcy Court For The District Of North Dakota",
          "U.S. Bankruptcy Court For The District Of Vermont",
          "U.S. Bankruptcy Court For The District Of Columbia",
          "U.S. Bankruptcy Court For The District Of Alaska",
          "U.S. Bankruptcy Court For The District Of Guam",
          "U.S. Bankruptcy Court For The District Of The Virgin Islands",
          "U.S. Bankruptcy Court For The District Of The Northern Mariana Islands"]


def _fill_text(el, search_key, search_params):
    if search_key in search_params:
        el.send_keys(search_params[search_key])
    
def _select_from_options(el, search_key, search_params):
    if search_key not in search_params:
        return
    search_value = search_params[search_key]
    for option in el.find_elements_by_tag_name('option'):
        if option.text.strip() == search_value:
            option.click()
            return

def _select_checkbox(el, search_key, search_params):
    if search_key in search_params and search_params[search_key] == "Select":
        el.click()
        
    
        
    
### TEST
    
def main():

    ###############################
    #### Login into the website ###
    ###############################

    # Make browser ready
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    service=Service(ChromeDriverManager().install())


    INPUT_FILE_PATH = "C://Users/Kevin/Desktop/Bloomberg_law/input.json"
    with open(INPUT_FILE_PATH, "r") as f:

        # Load Bloomberg Law account info
        queries = json.load(f)

        # Logging into the website
        browser.get("https://www.bloomberglaw.com/product/blaw/search/results/503b7fe442093008906e19ebeb2c9c0b")
        #browser.get("")
        username = browser.find_element(By.XPATH, "//*[@id='indg-username']")
        password = browser.find_element(By.XPATH, "//*[@id='indg-password']")
        _fill_text(username, "Username", search_params=queries[0])
        _fill_text(password, "Password", search_params=queries[0])
        browser.find_element(By.XPATH, "//*[@id='indg-submit']").click()
        time.sleep(5)


    ############################
    #### Test one sample web ###
    ############################

    # Load one sampleweb (Chapter 7 | U.S. Bankruptcy Court For The Central District Of California)
    browser.get("https://www.bloomberglaw.com/product/blaw/search/results/eccdf7307e80456ac1024608c201ace7")
    time.sleep(5)

    # Select single date
    temp = browser.find_elements(By.CLASS_NAME, 'selected')
    temp[1].click()
    browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[6]/div/div/div[3]/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[2]').click()
    time.sleep(5)

    # Fill in the date
    date = browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[6]/div/div/div[3]/div[1]/div/div[2]/div[2]/div/div[2]/div/span/label/input')
    _fill_text(date, 'Date', search_params=queries[0])
    browser.find_element(By.XPATH, "//body").click()
    time.sleep(5)
    
    # Test: Download csv results
    action = ActionChains(browser)
    download_menu = browser.find_element(By.CLASS_NAME,"DownloadDocumentsButton")
    download_button = browser.find_element(By.XPATH, '//*[@id="search-results-list-container"]/div[2]/div/div[2]/div/div[2]/span[1]/span/span[2]/span[2]/ul/li[2]/a')
    action.move_to_element(download_menu).perform()
    download_button.click()



    # 1. Loop through courts | Chapter 7
    for court in courts:
        
        print(court)
        count = 0

        ### The initial webpage for Chapter 7 on 4/6/2000 Date filed (court is not selected yet)
        browser.get("https://www.bloomberglaw.com/product/blaw/search/results/dd6afd8e05e688fac48e1503f9b4f929/")

        # show all courts
        show_more = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[6]/div/div/div[3]/div[1]/div/div[5]/div/div[2]/div[2]')))
        show_more.click()
        #browser.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[6]/div/div/div[3]/div[1]/div/div[5]/div/div[2]/div[2]").click()
        
        # Check next court
        try:
            next_court = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='" + court + "']")))
            next_court.click()
            count = count + 1
        except:
            # court not being found means that no filings for the date
            print("not filings for this court area on this date")
            continue
        #element = browser.find_element(By.XPATH, "//span[text()='" + court + "']")
        #element.click()
        
        ### Download
        time.sleep(3)
        action = ActionChains(browser)
        #download_menu = browser.find_element(By.CLASS_NAME, "DownloadDocumentsButton")
        download_menu = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "DownloadDocumentsButton")))
        #download_button = browser.find_element(By.XPATH, '//*[@id="search-results-list-container"]/div[2]/div/div[2]/div/div[2]/span[1]/span/span[2]/span[2]/ul/li[2]/a')
        action.move_to_element(download_menu).perform()
        download_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-results-list-container"]/div[2]/div/div[2]/div/div[2]/span[1]/span/span[2]/span[2]/ul/li[2]/a')))
        download_button.click()

        print("Filings have been downloaded:", court)
        time.sleep(5)




    # 2. Loop through courts | Chapter 11
    for court in courts:
        
        print(court)
        count = 0

        # The initial webpage for Chapter 11 on 4/6/2000 Date filed (court is not selected yet)
        browser.get("https://www.bloomberglaw.com/product/blaw/search/results/9a6ff3e2dc991ed3c96d6736cd76ebaa/")

        # show all courts
        show_more = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[6]/div/div/div[3]/div[1]/div/div[5]/div/div[2]/div[2]')))
        show_more.click()
        #browser.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[6]/div/div/div[3]/div[1]/div/div[5]/div/div[2]/div[2]").click()
        
        # Check next court
        try:
            next_court = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='" + court + "']")))
            next_court.click()
            count = count + 1
        except:
            # court not being found means that no filings for the date
            print("not filings for this court area on this date")
            continue
        #element = browser.find_element(By.XPATH, "//span[text()='" + court + "']")
        #element.click()
        
        ### Download
        time.sleep(5)
        action = ActionChains(browser)
        #download_menu = browser.find_element(By.CLASS_NAME, "DownloadDocumentsButton")
        download_menu = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "DownloadDocumentsButton")))
        #download_button = browser.find_element(By.XPATH, '//*[@id="search-results-list-container"]/div[2]/div/div[2]/div/div[2]/span[1]/span/span[2]/span[2]/ul/li[2]/a')
        action.move_to_element(download_menu).perform()
        download_button = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-results-list-container"]/div[2]/div/div[2]/div/div[2]/span[1]/span/span[2]/span[2]/ul/li[2]/a')))
        download_button.click()

        print("Filings have been downloaded:", court)



    # 3. Loop through courts | Chapter 13
    for court in courts:
        
        print(court)
        count = 0

        # The initial webpage for Chapter 13 on 4/6/2000 Date filed (court is not selected yet)
        browser.get("https://www.bloomberglaw.com/product/blaw/search/results/f93667d93f81c23e29769a7dbaa1c346/")

        # show all courts
        show_more = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[6]/div/div/div[3]/div[1]/div/div[5]/div/div[2]/div[2]')))
        show_more.click()
        #browser.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[6]/div/div/div[3]/div[1]/div/div[5]/div/div[2]/div[2]").click()
        
        # Check next court
        try:
            next_court = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='" + court + "']")))
            next_court.click()
            count = count + 1
        except:
            # court not being found means that no filings for the date
            print("not filings for this court area on this date")
            continue
        #element = browser.find_element(By.XPATH, "//span[text()='" + court + "']")
        #element.click()
        
        ### Download
        time.sleep(3)
        action = ActionChains(browser)
        #download_menu = browser.find_element(By.CLASS_NAME, "DownloadDocumentsButton")
        download_menu = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "DownloadDocumentsButton")))
        #download_button = browser.find_element(By.XPATH, '//*[@id="search-results-list-container"]/div[2]/div/div[2]/div/div[2]/span[1]/span/span[2]/span[2]/ul/li[2]/a')
        action.move_to_element(download_menu).perform()
        download_button = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-results-list-container"]/div[2]/div/div[2]/div/div[2]/span[1]/span/span[2]/span[2]/ul/li[2]/a')))
        download_button.click()

        print("Filings have been downloaded:", court)






if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python scrape_scrape.py <search query input file path> <chrome drivr path>")
        exit(1)
    # See expected input file format in README

    INPUT_FILE_PATH = sys.argv[1]
    DOWNLOAD_DIR_PATH = sys.argv[2]
    CHROME_DRIVER_PATH = sys.argv[3]
    main()
