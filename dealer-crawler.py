#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
dealer-crawler.py: crawls stage site from dealer perspective; simulates user 
activity and logs data
'''

__author__ = 'Trenton Bauer'
__version__ = 'V1.1'
__maintainer__ = 'Trenton Bauer'
__contact__ = 'trenton.bauer@gmail.com'
__status__ = 'Prototype'

import csv
import private
import secrets
import traceback
from array import array
from datetime import datetime
from time import localtime, strftime
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

# time script started running
kickoff = datetime.now()

# initialize browser options
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True

# create new Firefox driver and retreive login site
driver = webdriver.Firefox(options = fireFoxOptions, service=
    Service(GeckoDriverManager().install()))
driver.implicitly_wait(60)

try:
    driver.get(private.loginURL)

    # login to site
    username = driver.find_element(By.XPATH, '//input[@id="Email"]')
    username.clear()
    key = private.dealerUser
    username.send_keys(key)

    password = driver.find_element(By.XPATH, '//input[@id="Password"]')
    password.clear()
    key = private.dealerPass
    password.send_keys(key)

    submit= driver.find_element(By.XPATH, '//input[@type="submit"]')
    submit.click()
except:
    traceback.print_exc()
    print('EXCEPTION CAUGHT ON LOGIN')

# homepage fields to scrape
assignedOnline = []
assignedOffline = []
assignedInactive = []
unassigned = []
totalDealers = []

'''
append_home_arrays appends a given value to all arrays which represent data 
    fields found on the homepage.

:param txt: that which is to be appended to the arrays 
'''
def append_home_arrays(txt):
    assignedOnline.append(txt)
    assignedOffline.append(txt)
    assignedInactive.append(txt)
    unassigned.append(txt)
    totalDealers.append(txt)

'''
scrape_home scrapes data from the homepage and appends it to corresponding 
    arrays.

:param s: a Beautiful Soup object with the home page's source
'''
def scrape_home(s: bs):
    # append timestamp, unit MAC address, and unit name
    curTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    append_home_arrays(curTime)
    append_home_arrays('N/A')
    append_home_arrays('N/A')

    # append field labels
    assignedOnline.append('Assigned Valves: Online')
    assignedOffline.append('Assigned Valves: Offline')
    assignedInactive.append('Assigned Valves: Inactive')
    unassigned.append('Unassigned Valves')
    totalDealers.append('Total Dealers')

    # array of values found on homepage
    homeValues = []

    # scrape values from homepage and add to array
    for x in s.find_all('h5'):
        homeValues.append(str(x.text))
    
    # append data from homepage
    assignedOnline.append(str(homeValues[0]))
    assignedOffline.append(str(homeValues[1]))
    assignedInactive.append(str(homeValues[2]))
    unassigned.append(str(homeValues[3]))
    totalDealers.append(str(homeValues[4]))

 
try:
    # driver at homepage
    driver.get(private.homeURL)
    soup=bs(driver.page_source, 'html.parser')

    # check for timeout
    if soup.find('form',{'id':'CatchAllForm'}) == None:
        # scrape data from homepage
        scrape_home(soup)
    else:
        append_home_arrays(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        append_home_arrays('ERROR:')
        append_home_arrays(soup.find('p',{'id':'ErrorNumber'}).text)
except:
    traceback.print_exc()
    print('EXCEPTION CAUGHT WHILE SCRAPING HOME')

# unit page fields to scrape
unitErrors = []
usageChartHour = []
capRemGraph = []
usageChartDay = []

'''
append_unit_arrays appends a given value to all arrays which represent data 
    fields found on the unit page.

:param txt: that which is to be appended to the arrays
'''
def append_unit_arrays(txt):
    unitErrors.append(txt)
    usageChartHour.append(txt)
    usageChartDay.append(txt)
    capRemGraph.append(txt)

'''
scrape_unit scrapes data from a given unit page and appends it to corresponding 
    arrays.

:param s: a Beautiful Soup object with a unit page's source
'''
def scrape_unit(s: bs):
    # append timestamp, unit MAC address, and unit name
    curTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    append_unit_arrays(curTime)
    append_unit_arrays(randMac)
    append_unit_arrays(s.find('p',class_='font-weight-bold').text.strip())

    # append field labels
    unitErrors.append('Valve Status')
    usageChartHour.append('Hourly Usage')
    usageChartDay.append('Average Daily Usage')
    capRemGraph.append('Daily Capacity Remaining')

    # append number of errors on unit
    unitErrors.append(s.find('span',class_='text-nowrap').text.strip())
    
    # append data from javascript charts/graphs
        # hourly usage chart
    if s.find('canvas',{'id':'hourlyWaterUsageChart'}) != None:
        append_dict(s.find('canvas',{'id':'hourlyWaterUsageChart'})
            .find_next_sibling().text,usageChartHour)
    else:
        usageChartHour.append('data not populated')

        # cap rem graph
    if s.find('canvas',{'id':'remainingCapacityChart'}) != None:
        append_dict(s.find('canvas',{'id':'remainingCapacityChart'})
            .find_next_sibling().text,capRemGraph)
    else:
        capRemGraph.append('data not populated')

        # daily usage chart
    if s.find('canvas',{'id':'dailyWaterUsageChart'}) != None:
        append_dict(s.find('canvas',{'id':'dailyWaterUsageChart'})
            .find_next_sibling().text,usageChartDay)
    else:
        usageChartDay.append('data not populated')

'''
append_dict creates a dictionary from javascript content found on the unit page 
    by extracting corresponding "labels" and "data" fields from given text, then 
    appends that dictionary to a given array

:param script: text from within javascript tags on the unit page
:param arr: array to which the dictionary is appended
'''
def append_dict (script: str, arr: array):
    labels = script[(script.find('labels:') + 10) : (script.find( '],', 
        script.find('labels:')) - 1)].split('","')
    data = script[(script.find('data: [') + 7) : script.find( '],', 
        script.find('data: ['))].split(',')
    arr.append(dict(zip(labels,data)))

try:
    # driver at random unit page
    randMac = secrets.choice(private.macArray)
    driver.get(private.unitURL + randMac)
    soup=bs(driver.page_source,'html.parser')

    # check for timeout
    if soup.find('form',{'id':'CatchAllForm'}) == None:
        # scrape data from unit page
        scrape_unit(soup)
    else:
        append_unit_arrays(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        append_unit_arrays(randMac)
        append_unit_arrays('ERROR:')
        append_unit_arrays(soup.find('p',{'id':'ErrorNumber'}).text)
except:
    traceback.print_exc()
    print('EXCEPTION CAUGHT WHILE SCRAPING UNIT')

'''
writeToCSV writes arrays to a CSV file as rows

:param path: path to CSV file
:param delim: string delimiter for writing arrays to rows
:param *args: variable number of array arguments to be written to given CSV
'''
def writeToCSV(path: str, delim: str, *args : array):
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=delim)
        for x in args:
            writer.writerow(x)    
    file.close()

# write scraped data to CSV
writeToCSV(private.wdFilePath, ',', assignedOnline, assignedOffline, 
    assignedInactive, unassigned, totalDealers, unitErrors, usageChartHour, 
    usageChartDay, capRemGraph)

# close the webdriver
driver.close()

# print execution runtime
td = datetime.now() - kickoff
print('Execution took ' + str(td.total_seconds()) + ' seconds.')

# indicate completion
print('Complete.\n')
