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
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

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


