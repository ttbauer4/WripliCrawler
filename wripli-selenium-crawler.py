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

import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from openpyxl.workbook import Workbook

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
driver.get('https://wripli.com/Account/Login?ReturnUrl=%\2F&id=loginForm')
time.sleep(3)

username = driver.find_element(By.XPATH, '//input[@id="Email"]')
username.clear()
username.send_keys('trenton.bauer@gmail.com')

password = driver.find_element(By.XPATH, '//input[@id="Password"]')
password.clear()
password.send_keys('P@ssw0rd')

submit= driver.find_element(By.XPATH, '//input[@type="submit"]')
submit.click()

content = driver.page_source
soup=BeautifulSoup(content,features="lxml")

homepage_titlecard_values = []
for x in soup.findAll('h5'):
    homepage_titlecard_values.append(x.text)

row_headers = ['Assigned Valves: Online', 'Assigned Valves: Offline', 'Assigned Valves: Inactive', 'Unassigned Valves', 'Total Dealers']
df = pd.DataFrame({'' : row_headers , 'Values' : homepage_titlecard_values})
df.to_excel('data.xlsx', index=False, encoding='utf-8')

driver.close()