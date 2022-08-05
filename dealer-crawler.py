#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
dealer-crawler.py: crawls stage site from dealer perspective; simulates user 
activity and logs data
'''

__author__ = 'Trenton Bauer'
__version__ = 'V1.3'
__maintainer__ = 'Trenton Bauer'
__contact__ = 'trenton.bauer@gmail.com'
__status__ = 'Development'

import sys, os
import csv
import json
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

# retreive user info from private.json
if getattr(sys,'frozen',False):
    filePath = sys._MEIPASS + '/' + 'private.json'
else:
    filePath = os.path.dirname(os.path.abspath(__file__)) + '/' + 'private.json'

with open(filePath, 'r') as f:
    credentials = json.load(f)
    dealerUser = credentials["Email"]
    dealerPass = credentials["Password"]

    macArray = credentials["Mac Array"]

    fileName = credentials["File Name"]

    loginURL = credentials["login URL"]
    homeURL = credentials["home URL"]
    unitURL = credentials["unit URL"]

# set output file path
if getattr(sys,'frozen',False):
    filePath = sys._MEIPASS + '/' + fileName
else:
    filePath = os.path.dirname(os.path.abspath(__file__)) + '/' + fileName

'''
reset removes any existing WripliData.csv file in the same directory then
    initializes a new one
'''
def reset():
    # remove existing file
    if (os.path.exists(filePath) and os.path.isfile(filePath)):
        os.remove(filePath)
        print('\nfile deleted')
    else:
        print('\nfile not found')

    # create new file with headers
    file = open(filePath, 'w')
    file.write('TIMESTAMP,MAC ADDRESS,UNIT NAME,FIELD,VALUE\n')
    print(fileName + ' created')
    file.close()

# check for command line arguments
# command line arguments absent
if len(sys.argv) == 1:
    # prompt user selection
    i = input('\nWould you like to:\n(1) get data from a random unit\n(2) get '+ 
              'data from all units\n(3) get data from a specific unit\n(4) ' + 
              'reset the datasheet\n(5) quit\n\n')

    # check for valid input
    while i != '1' and i != '2' and i != '3' and i != '4' and i != '5':
        i = input('invalid input, enter \'1\' or \'2\' or \'3\' or \'4\' or \'5\'\n')

    # reset datasheet loop
    while i == '4':
        reset()
        i = input('\nWould you like to:\n(1) get data from a random unit\n(2) '+ 
                  'get data from all units\n(3) get data from a specific unit' +
                  '\n(4) reset the datasheet\n(5) quit\n\n')
        while i != '1' and i != '2' and i != '3' and i != '4' and i != '5':
            i = input('invalid input, enter \'1\' or \'2\' or \'3\' or \'4\' or \'5\'\n')
    
    # quit program
    if i == '5':
        print('\nComplete.\n')
        sys.exit()

    # prompt user to input MAC address
    if i == '3':
        mac = input('Enter the unit\'s MAC address:\n')
        valid = False
        for x in macArray:
            if x == mac:
                valid = True
        while not valid:
            mac = input('invalid mac address not found in macArray; try again:\n')
            for x in macArray:
                if x == mac:
                    valid = True

    # time script started running
    kickoff = datetime.now()

# command line arguments present
else:
    # time script started running
    kickoff = datetime.now()

    # assign command line arg to i
    i = sys.argv[1]

    # assign command line arg to mac if sys.argv[1] is 3
    if i == '3':
        mac = sys.argv[2]

# initialize browser options
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True

# create new Firefox driver and retreive login site
driver = webdriver.Firefox(options=fireFoxOptions, service=
    Service(GeckoDriverManager().install()))
driver.implicitly_wait(60)

try:
    # login to site
    driver.get(loginURL)

    username = driver.find_element(By.XPATH, '//input[@id="Email"]')
    username.clear()
    username.send_keys(dealerUser)

    password = driver.find_element(By.XPATH, '//input[@id="Password"]')
    password.clear()
    password.send_keys(dealerPass)

    submit = driver.find_element(By.XPATH, '//input[@type="submit"]')
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
    driver.get(homeURL)
    soup = bs(driver.page_source, 'html.parser')

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
totalUsage = []
usage = []
maxFlow = []
flags = []
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
    totalUsage.append(txt)
    usage.append(txt)
    maxFlow.append(txt)
    flags.append(txt)
    usageChartHour.append(txt)
    usageChartDay.append(txt)
    capRemGraph.append(txt)

'''
append_dict_tab creates a dictionary given headers and data from a table and
appends it to the given array

:param h: array of headers
:param d: array of data
:param arr: array to which the dictionary is appended
'''
def append_dict_tab(h: array, d: array, arr: array):
    arr.append(dict(zip(h,d)))

'''
scrape_unit scrapes data from a given unit page and appends it to corresponding 
    arrays.

:param s: a Beautiful Soup object with a unit page's source
'''
def scrape_unit(s: bs):
    unitErrors.clear()
    totalUsage.clear()
    usage.clear()
    maxFlow.clear()
    flags.clear()
    usageChartHour.clear()
    usageChartDay.clear()
    capRemGraph.clear()


    # append timestamp, unit MAC address, and unit name
    curTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    append_unit_arrays(curTime)
    append_unit_arrays(mac)
    append_unit_arrays(s.find('p',class_='font-weight-bold').text.strip())

    # append field labels
    unitErrors.append('Valve Status')
    totalUsage.append('Total Usage')
    usage.append('Usage')
    maxFlow.append('Max Flow')
    flags.append('Flags')
    usageChartHour.append('Hourly Usage')
    usageChartDay.append('Average Daily Usage')
    capRemGraph.append('Daily Capacity Remaining')

    # append number of errors on unit
    unitErrors.append(s.find('span',class_='text-nowrap').text.strip())

    # find rows in the general data table
    tableRows = s.find('table',{'id':'DailyGeneralDataTable'}).find('tbody').find_all('tr')

    # find headers in the general data table (dates ONLY)
    tableHeaders = []
    for x in s.find('table',{'id':'DailyGeneralDataTable'}).find('thead').find('tr').find_all('th'):
        tableHeaders.append(x.get_text().replace('\n',''))
    del tableHeaders[:2]

    # append total usage (in gallons) this week
    totalUsage.append(tableRows[0].find_all('th')[1].text)

    # append usage data for this week
    td=[]
    for x in tableRows[0].find_all('td'):
        td.append(x.get_text().replace('\n',''))
    append_dict_tab(tableHeaders, td, usage)

    # append max flow data for this week
    td=[]
    for x in tableRows[1].find_all('td'):
        td.append(x.get_text().replace('\n',''))
    append_dict_tab(tableHeaders, td, maxFlow)

    # append flag data for this week
    td=[]
    for x in tableRows[2].find_all('td'):
        td.append(x.get_text().replace('\n',''))
    append_dict_tab(tableHeaders, td, flags)

    # append data from javascript charts/graphs
    # hourly usage chart
    if s.find('canvas',{'id':'hourlyWaterUsageChart'}) != None:
        append_dict_js(s.find('canvas',{'id':'hourlyWaterUsageChart'})
                        .find_next_sibling().text,usageChartHour)
    else:
        usageChartHour.append('data not populated')

    # cap rem graph
    if s.find('canvas',{'id':'remainingCapacityChart'}) != None:
        append_dict_js(s.find('canvas',{'id':'remainingCapacityChart'})
                        .find_next_sibling().text,capRemGraph)
    else:
        capRemGraph.append('data not populated')

    # daily usage chart
    if s.find('canvas',{'id':'dailyWaterUsageChart'}) != None:
        append_dict_js(s.find('canvas',{'id':'dailyWaterUsageChart'})
                        .find_next_sibling().text,usageChartDay)
    else:
        usageChartDay.append('data not populated')

'''
append_dict_js creates a dictionary from javascript content found on the unit page 
    by extracting corresponding "labels" and "data" fields from given text, then 
    appends that dictionary to a given array

:param script: text from within javascript tags on the unit page
:param arr: array to which the dictionary is appended
'''
def append_dict_js (script: str, arr: array):
    labels = script[(script.find('labels:') + 10) : (script.find( '],', 
                    script.find('labels:')) - 1)].split('","')
    data = script[(script.find('data: [') + 7) : script.find( '],', 
                  script.find('data: ['))].split(',')
    arr.append(dict(zip(labels,data)))

'''
writeToCSV writes arrays to a CSV file as rows

:param path: path to CSV file
:param delim: string delimiter for writing arrays to rows
:param *args: variable number of array arguments to be written to given CSV
'''
def write_to_csv(path: str, delim: str, *args : array):
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=delim)
        for x in args:
            writer.writerow(x)    
        file.close()

# write homepage data to CSV
write_to_csv(filePath, ',', assignedOnline, assignedOffline, 
    assignedInactive, unassigned, totalDealers)

# get data from a random unit
if i == '1':
    try:
        # driver at random unit page
        mac = secrets.choice(macArray)
        driver.get(unitURL + mac)
        soup = bs(driver.page_source,'html.parser')

        # check for timeout
        if soup.find('form',{'id':'CatchAllForm'}) == None:
            # scrape data from unit page
            scrape_unit(soup)
        else:
            append_unit_arrays(strftime("%Y-%m-%d %H:%M:%S", localtime()))
            append_unit_arrays(mac)
            append_unit_arrays('ERROR:')
            append_unit_arrays(soup.find('p',{'id':'ErrorNumber'}).text)
        
        # write scraped data to CSV
        write_to_csv(filePath, ',', unitErrors, totalUsage, usage, 
            maxFlow, flags, usageChartHour, usageChartDay, capRemGraph)
    except:
        traceback.print_exc()
        print('EXCEPTION CAUGHT WHILE SCRAPING UNIT')

# get data from all units
elif i == '2':
    try:
        for x in macArray:
            # driver at given unit page
            mac = x
            driver.get(unitURL + mac)
            soup = bs(driver.page_source,'html.parser')

            # check for timeout
            if soup.find('form',{'id':'CatchAllForm'}) == None:
                # scrape data from unit page
                scrape_unit(soup)
            else:
                append_unit_arrays(strftime("%Y-%m-%d %H:%M:%S", localtime()))
                append_unit_arrays(mac)
                append_unit_arrays('ERROR:')
                append_unit_arrays(soup.find('p',{'id':'ErrorNumber'}).text)
            
            # write scraped data to CSV
            write_to_csv(filePath, ',', unitErrors, totalUsage, usage, 
                maxFlow, flags, usageChartHour, usageChartDay, capRemGraph)
    except:
        traceback.print_exc()
        print('EXCEPTION CAUGHT WHILE SCRAPING UNIT')

# get data from a specific unit
elif i == '3':
    try:
        # driver at given unit page
        driver.get(unitURL + mac)
        soup = bs(driver.page_source,'html.parser')

        # check for timeout
        if soup.find('form',{'id':'CatchAllForm'}) == None:
            # scrape data from unit page
            scrape_unit(soup)
        else:
            append_unit_arrays(strftime("%Y-%m-%d %H:%M:%S", localtime()))
            append_unit_arrays(mac)
            append_unit_arrays('ERROR:')
            append_unit_arrays(soup.find('p',{'id':'ErrorNumber'}).text)
        
        # write scraped data to CSV
        write_to_csv(filePath, ',', unitErrors, totalUsage, usage, 
            maxFlow, flags, usageChartHour, usageChartDay, capRemGraph)
    except:
        traceback.print_exc()
        print('EXCEPTION CAUGHT WHILE SCRAPING UNIT')

# invalid command line argument
else:
    print('INVALID COMMAND LINE ARGUMENT: UNABLE TO DETERMINE WHICH UNITS TO SCRAPE')

# close the webdriver
driver.close()

# print execution runtime
td = datetime.now() - kickoff
print('Execution took ' + str(td.total_seconds()) + ' seconds.')

# indicate completion
print('Complete.\n')
