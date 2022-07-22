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

import secrets
import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

url = 'https://www.wripli.com'

session = requests.session()

csrf_token = session.get(url).cookies['__RequestVerificationToken']
payload = {
    'Email' : 'trenton.bauer@gmail.com',
    'Password' : 'P@ssw0rd',
    'csrfmiddlewaretoken' : csrf_token
}

login_req = session.post(url + '/Account/Login?ReturnUrl=%2F', data = payload)

# Verify successful login
print(login_req.status_code)

# Save login cookies
cookies = login_req.cookies

### Begin Scrape ###
sample = ['4C11AEF90AB0']

random_valve = secrets.choice(sample)
soup = BeautifulSoup(session.get(url + '/Editor/Performance/?macAddress=').text + random_valve, 'html.parser')

# Verify successful page navigation
print(soup.find('div', {'class','row pgcontent'}))