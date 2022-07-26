#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' crawler.py: crawls Wripli stage site;
    simulates daily user activity and logs data
    automated web scraping process run regularly
'''

__author__ = 'Trenton Bauer'
__version__ = '1.0.0'
__email__ = 'trenton.bauer@gmail.com'
__status__ = 'Development'

import pandas as pd
from time import localtime, strftime
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# make Firefox headless
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True

# create new Firefox driver and retreive login site
driver = webdriver.Firefox(options = fireFoxOptions, service=Service(GeckoDriverManager().install()))
driver.get('https://wripli.com/Account/Login?ReturnUrl=%\2F&id=loginForm')

# login to Wripli site
username = driver.find_element(By.XPATH, '//input[@id="Email"]')
username.clear()
username.send_keys('trenton.bauer@gmail.com')

password = driver.find_element(By.XPATH, '//input[@id="Password"]')
password.clear()
password.send_keys('P@ssw0rd')

submit= driver.find_element(By.XPATH, '//input[@type="submit"]')
submit.click()

# driver at homepage; create new bs object
content = driver.page_source
soup=bs(content,features="lxml")

timestamp = []
row_headers = ['Assigned Valves: Online', 'Assigned Valves: Offline', 'Assigned Valves: Inactive', 'Unassigned Valves', 'Total Dealers']
homepage_titlecard_values = []
for x in soup.findAll('h5'):
    homepage_titlecard_values.append(x.text)
    timestamp.append(strftime("%Y-%m-%d %H:%M:%S", localtime()))

filePath = 'WripliData.xlsx'
wb = load_workbook(filePath)
writer = pd.ExcelWriter(filePath, engine = 'openpyxl', mode='a', if_sheet_exists = 'overlay')
writer.book = wb
df1 = pd.DataFrame({'Time (YYYY-MM-DD HH:MM:SS)' : timestamp ,'Category' : row_headers , 'Values' : homepage_titlecard_values})
df1.to_excel(writer, sheet_name='Homepage', index=False)
writer.save()
writer.close()

driver.close()