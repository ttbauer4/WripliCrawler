#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
dealer-crawler.py: crawls stage site from dealer perspective; simulates user 
activity and logs data
'''

__author__ = 'Trenton Bauer'
__version__ = 'V1.4'
__maintainer__ = 'Trenton Bauer'
__contact__ = 'trenton.bauer@gmail.com'
__status__ = 'Development'

import sys, os
import csv
import json
import secrets
import cursor
import traceback
import time
from array import array
from datetime import datetime
from time import localtime, strftime
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium import common
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

# retreive user info from private.json
if getattr(sys,'frozen',False):
    filePath = sys._MEIPASS + '/' + 'private.json'
else:
    filePath = os.path.dirname(os.path.abspath(__file__)) + '/' + 'private.json'

try: 
    with open(filePath, 'r') as f:
        credentials = json.load(f)
        dealerUser = credentials["Email"]
        dealerPass = credentials["Password"]

        macArray = credentials["Mac Array"]

        fileName = credentials["File Name"]

        loginURL = credentials["login URL"]
        homeURL = credentials["home URL"]
        perfURL = credentials["performance URL"]
        consumURL = credentials["consumer URL"]
except:
    traceback.print_exc()
    print('\nEXCEPTION CAUGHT WHILE LOADING INFO FROM private.json. MAKE SURE:')
    print('  - private.json IS IN THE SAME FOLDER/DIRECTORY AS dealer-crawler')
    print('  - private.json IS PROPERLY FORMATTED (SEE https://www.w3schools.com/js/js_json_syntax.asp FOR MORE INFO)')
    print('  - private.json CONTAINS THE FIELDS \"Email\", \"Password\", \"Mac Array\", \"File Name\", \"login URL\", \"home URL\", \"performance URL\", AND \"consumer URL\"\n')
    cursor.show()
    e = input('press \'Enter\' to exit or close this window.\n')
    if e != None:
        sys.exit()

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
    try:
    # remove existing file
        if (os.path.exists(filePath) and os.path.isfile(filePath)):
            os.remove(filePath)
            print('\nfile deleted')
        else:
            print('\nfile not found')
    except:
        traceback.print_exc()
        print('EXCEPTION CAUGHT ON RESET: ENSURE THAT ' + fileName + ' IS NOT OPEN ON YOUR COMPUTER\n')
        cursor.show()
        e = input('press \'Enter\' to exit or close this window.\n')
        if e != None:
            sys.exit()

    # create new file with headers
    file = open(filePath, 'w')
    file.write('TIMESTAMP,MAC ADDRESS,UNIT NAME,FIELD,VALUE\n')
    print(fileName + ' created')
    file.close()

# check for command line arguments
if len(sys.argv) == 1: # command line arguments absent
    # prompt user selection
    i = input('\nWould you like to:\n(1) get data from a random unit\n(2) get '+ 
              'data from all units\n(3) get data from a specific unit\n(4) ' + 
              'reset the datasheet\n(5) quit\n\n')

    # check for valid input
    while i != '1' and i != '2' and i != '3' and i != '4' and i != '5':
        i = input('invalid input, enter \'1\' or \'2\' or \'3\' or \'4\' or \'5\'\n')

    while i == '4': # reset datasheet loop
        reset()
        i = input('\nWould you like to:\n(1) get data from a random unit\n(2) '+ 
                  'get data from all units\n(3) get data from a specific unit' +
                  '\n(4) reset the datasheet\n(5) quit\n\n')
        while i != '1' and i != '2' and i != '3' and i != '4' and i != '5':
            i = input('invalid input, enter \'1\' or \'2\' or \'3\' or \'4\' or \'5\'\n')
    
    if i == '5': # quit program
        print('\nComplete.\n')
        cursor.show()
        sys.exit()
    
    if i == '3': # prompt user to input MAC address
        mac = input('Enter the unit\'s MAC address:\n')
        valid = False
        for x in macArray:
            if x == mac:
                valid = True
        while not valid:
            mac = input('invalid mac address not found in Mac Array; try again:\n')
            for x in macArray:
                if x == mac:
                    valid = True

    # time script started running
    kickoff = datetime.now()

else: # command line arguments present
    # time script started running
    kickoff = datetime.now()

    # assign command line arg to i
    i = sys.argv[1]

    # assign command line arg to mac if sys.argv[1] is 3
    if i == '3':
        mac = sys.argv[2]

# hide cursor in console window
cursor.hide()

try:
    # initialize browser options
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.headless = True
    fireFoxOptions.page_load_strategy = 'eager'

    # create new Firefox driver and retreive login site
    driver = webdriver.Firefox(options=fireFoxOptions, service=
        Service(GeckoDriverManager().install()))

    # set timeout
    driver.set_page_load_timeout(60)

except:
    traceback.print_exc()
    print('\nEXCEPTION CAUGHT ON LOGIN. MAKE SURE:')
    print('  - YOU HAVE INSTALLED MOZILLA FIREFOX FROM https://www.mozilla.org/en-US/firefox/new/')
    print('  - YOUR DEVICE IS CONNECTED TO THE INTERNET\n')
    cursor.show()
    e = input('press \'Enter\' to exit or close this window.\n')
    if e != None:
        sys.exit()

try:
    # initialize progress %
    print('0.00%', end='\r')

    # initialize progress variables
    prog = 0.0
    total = 0.0

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

except common.TimeoutException:
    traceback.print_exc()
    print('LOGIN PAGE REACHED MAX LOAD TIME OF 60 SECONDS. PLEASE CHECK:')
    print('  - YOUR NETWORK CONNECTION')
    print('  - THAT ' + driver.current_url + ' IS NOT UNDER MAINTENANCE\n')
    cursor.show()
    e = input('press \'Enter\' to exit or close this window.\n')
    if e != None:
        sys.exit()
except:
    traceback.print_exc()
    print('EXCEPTION CAUGHT ON LOGIN: ENSURE PRIVATE.JSON CONTAINS THE ACCURATE LOGIN PAGE URL\n')
    cursor.show()
    e = input('press \'Enter\' to exit or close this window.\n')
    if e != None:
        sys.exit()

'''
append_all appends a given value to each array within an array.

:param txt: that which is to be appended to the arrays 
:param arr: an array of arrays to which txt is appended
'''
def append_all(txt:str, arr:array):
    for x in arr:
        x.append(txt)

'''
append_dict_tab creates a dictionary given headers and data from a table and
appends it to the given array

:param h: array of headers
:param d: array of data
:param arr: array to which the dictionary is appended
'''
def append_dict_tab(h: array, d: array, arr: array):
    if bool(dict(zip(h,d))):    
        arr.append(dict(zip(h,d)))
    else:
        arr.append('data not populated')

'''
append_dict_js creates a dictionary from javascript content found on the performance
    page by extracting corresponding "labels" and "data" fields from given text, then 
    appends that dictionary to a given array

:param script: text from within javascript tags on the performance page
:param arr: array to which the dictionary is appended
'''
def append_dict_js (script: str, arr: array):
    labels = script[(script.find('labels:') + 10) : (script.find( '],', 
                    script.find('labels:')) - 1)].split('","')
    data = script[(script.find('data: [') + 7) : script.find( '],', 
                  script.find('data: ['))].split(',')
    if bool(dict(zip(labels,data))):
        arr.append(dict(zip(labels,data)))
    else:
        arr.append('data not populated')
'''
write_to_csv writes arrays to a CSV file as rows

:param path: path to CSV file
:param delim: string delimiter for writing arrays to rows
:param *args: variable number of array arguments to be written to given CSV
'''
def write_to_csv(path: str, delim: str, *args : array):
    try:
        with open(path, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=delim)
            for x in args:
                writer.writerow(x)    
            file.close()
    except:
        traceback.print_exc()
        print('EXCEPTION CAUGHT WHILE TRYING TO WRITE TO ' + fileName + ', ENSURE THAT IT IS NOT OPEN ON YOUR COMPUTER\n')
        cursor.show()
        e = input('press \'Enter\' to exit or close this window.\n')
        if e != None:
            sys.exit()

# homepage fields to scrape
assignedOnline = []
assignedOffline = []
assignedInactive = []
unassigned = []
totalDealers = []
homeArrays = [assignedOnline, assignedOffline, assignedInactive, unassigned, totalDealers]

# performance page fields to scrape
unitErrors = []
totalUsage = []
usage = []
maxFlow = []
flags = []
usageChartHour = []
capRemGraph = []
usageChartDay = []
brineTable = []
ozoneTable = []
perfArrays = [unitErrors, totalUsage, usage, maxFlow, flags, usageChartHour, capRemGraph, usageChartDay, brineTable, ozoneTable]

# consumer view fields to scrape
currFlowIcon = []
usageTodayIcon = []
peakFlowRateIcon = []
capRemIcon = []
rssi = []
consumArrays = [currFlowIcon, usageTodayIcon, peakFlowRateIcon, capRemIcon, rssi]

'''
scrape_home scrapes data from the homepage and appends it to corresponding 
    arrays.

:param s: a Beautiful Soup object with the home page's source
'''
def scrape_home(s: bs):
    # append timestamp, unit MAC address, and unit name
    curTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    append_all(curTime, homeArrays)
    append_all('N/A', homeArrays)
    append_all('N/A', homeArrays)

    # append field labels
    assignedOnline.append('Assigned Valves: Online')
    assignedOffline.append('Assigned Valves: Offline')
    assignedInactive.append('Assigned Valves: Inactive')
    unassigned.append('Unassigned Valves')
    totalDealers.append('Total Dealers')

    # array of values found on homepage
    homeValues = []

    # scrape values from homepage and add to array
    if len(s.find_all('h5')) >= 5:
        for x in s.find_all('h5'):
            if x != None:
                homeValues.append(str(x.text))
            else:
                homeValues.append('error')  
    else:
        homeValues.append('error finding all homepage data')
        homeValues.append('error finding all homepage data')
        homeValues.append('error finding all homepage data')
        homeValues.append('error finding all homepage data')
        homeValues.append('error finding all homepage data')
    
    # append data from homepage
    assignedOnline.append(str(homeValues[0]))
    assignedOffline.append(str(homeValues[1]))
    assignedInactive.append(str(homeValues[2]))
    unassigned.append(str(homeValues[3]))
    totalDealers.append(str(homeValues[4]))

'''
scrape_perf scrapes data from a given unit's performance page and appends it to corresponding 
    arrays.

:param s: a Beautiful Soup object with a performance page's source
'''
def scrape_perf(s: bs):
    global mac

    unitErrors.clear()
    totalUsage.clear()
    usage.clear()
    maxFlow.clear()
    flags.clear()
    usageChartHour.clear()
    usageChartDay.clear()
    capRemGraph.clear()
    brineTable.clear()
    ozoneTable.clear()

    # append timestamp, unit MAC address, and unit name
    curTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    append_all(curTime, perfArrays)
    append_all(mac, perfArrays)
    append_all(s.find('p',class_='font-weight-bold').text.strip(), perfArrays)

    # append field labels
    unitErrors.append('Valve Status')
    totalUsage.append('Total Usage')
    usage.append('Usage')
    maxFlow.append('Max Flow')
    flags.append('Flags')
    usageChartHour.append('Hourly Usage')
    usageChartDay.append('Average Daily Usage')
    capRemGraph.append('Daily Capacity Remaining')
    brineTable.append('Brine % (Last 10 Regens)')
    ozoneTable.append('Ozone Milliamps (Last 10 Regens)')

    # append number of errors on unit
    status = s.find('span',class_='text-nowrap').text.strip()
    if status != '0 Errors':
        errs = s.find('div',{'id':'valveStatus-Performance'}).find_all('p')[2:]
        status += ': '
        for x in errs:
            status += x.text + ', '
        status = status[:-2]
    unitErrors.append(status)


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

    # append data from cap rem graph
    if s.find('canvas',{'id':'remainingCapacityChart'}) != None:
        append_dict_js(s.find('canvas',{'id':'remainingCapacityChart'})
                        .find_next_sibling().text,capRemGraph)
    else:
        capRemGraph.append('data not populated')

    # append data from daily usage chart
    if s.find('canvas',{'id':'dailyWaterUsageChart'}) != None:
        append_dict_js(s.find('canvas',{'id':'dailyWaterUsageChart'})
                        .find_next_sibling().text,usageChartDay)
    else:
        usageChartDay.append('data not populated')

    # find rows in the regen data table
    tableRows = s.find('table', class_='table table-striped table-sm dataTable no-footer regen-brine').find('tbody').find_all('tr')
    
    # find headers in the regen data table (dates ONLY)
    tableHeaders = []
    for x in s.find('table',class_='table table-striped table-sm dataTable no-footer regen-brine').find('thead').find('tr').find_all('td'):
        tableHeaders.append(x.get_text())
    
    # append brine % data
    td = []
    for x in tableRows[0].find_all('td'):
        td.append(x.get_text())
    append_dict_tab(tableHeaders, td, brineTable)

    # append ozone milliamps data
    td = []
    for x in tableRows[1].find_all('td'):
        td.append(x.get_text())
    append_dict_tab(tableHeaders, td, ozoneTable)

'''
scrape_consumer scrapes data from the consumer page of a given unit and appends it to corresponding 
    arrays.

:param s: a Beautiful Soup object with a unit's consumer page source
'''
def scrape_consumer(s:bs):
    global mac

    currFlowIcon.clear()
    usageTodayIcon.clear()
    peakFlowRateIcon.clear()
    capRemIcon.clear()
    rssi.clear()

    # append timestamp, unit MAC address, and unit name
    curTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    append_all(curTime, consumArrays)
    append_all(mac, consumArrays)
    append_all(s.find('p',class_='font-weight-bold').text.strip(), consumArrays)

    # append field labels
    currFlowIcon.append('Current Flow Rate')
    usageTodayIcon.append('Gallons Used Today')
    peakFlowRateIcon.append('Peak Flow Rate-Last 7 Days')
    capRemIcon.append('Capacity Remaining Until Regen')
    rssi.append('RSSI (Signal Strength)')

    # append current flow rate
    currFlowIcon.append(s.find('div',{'id':'divCurrentFlowRate'}).text)

    # append today's usage
    usageTodayIcon.append(s.find('div',{'id':'todaysWaterUsage'}).find('div', class_='stat-number font-weight-bold').text)

    # append peak flow rate
    peakFlowRateIcon.append(s.find('div',{'id':'pastWeekPeakFlowRate'}).find('div', class_='stat-number font-weight-bold').text)

    # append capacity remaining
    capRemIcon.append(s.find('div',{'id':'divCapacityRemaining'}).text)

    # append RSSI
    sig = s.find('img',{'id':'valveSignalStrengthImg'})['src']
    sig = sig[sig.find('_')+1:-4].replace('_',': ').replace('bar', ' bar')
    rssi.append(sig)

'''
crawl_unit crawls the unit pages of a given mac address using a given webdriver object

:param addr: the mac address whose pages are to be scraped
:param d: the webdriver to use when crawling the unit pages
'''
def crawl_unit(addr: str, d: webdriver.Firefox):
    global prog, total

    # update progress output
    print(str("%.2f" % ((prog/total)*100.0)) + '%', end='\r')

    # driver at performance page
    d.get(perfURL + addr)
 
    # create new html parser
    soup = bs(d.page_source, 'html.parser')

    # check for timeout
    if soup.find('form',{'id':'CatchAllForm'}) == None: # scrape data from performance view
        scrape_perf(soup)
        prog+=1.0
        print(str("%.2f" % ((prog/total)*100.0)) + '%', end='\r')
    else: # performance page threw an error message, output error onto sheet
        append_all((strftime("%Y-%m-%d %H:%M:%S", localtime())), perfArrays)
        append_all(addr, perfArrays)
        append_all('ERROR:', perfArrays)
        append_all(soup.find('p',{'id':'ErrorNumber'}).text, perfArrays)
        
    # driver at consumer page
    d.get(consumURL + addr)
    
    # wait for capacity remaining
    cri = d.find_element(By.XPATH, '//div[@id="divCapacityRemaining"]').text
    cr = cri
    y = 0
    while (cri == cr or cr == '0') and y < 7:
        time.sleep(1)
        cr = d.find_element(By.XPATH, '//div[@id="divCapacityRemaining"]').text
        y+=1
    soup = bs(d.page_source,'html.parser')

    # check for timeout
    if soup.find('form',{'id':'CatchAllForm'}) == None: # scrape data from consumer view
        scrape_consumer(soup)
        prog+=1.0
        print(str("%.2f" % ((prog/total)*100.0)) + '%', end='\r')
    else: # consumer page threw an error message, output error onto sheet
        append_all((strftime("%Y-%m-%d %H:%M:%S", localtime())), consumArrays)
        append_all(addr, consumArrays)
        append_all('ERROR:', consumArrays)
        append_all(soup.find('p',{'id':'ErrorNumber'}).text, consumArrays)

    # write unit data to CSV
    for x in perfArrays:
        write_to_csv(filePath, ',', x)
    for x in consumArrays:
        write_to_csv(filePath, ',', x)

# BEGIN CRAWLING
try:
    # driver at homepage
    if driver.find_element(By.XPATH, '//div[@id="WR_Cards"]') == None:
        driver.get(homeURL)
    soup = bs(driver.page_source, 'html.parser')

    # check for timeout
    if soup.find('form',{'id':'CatchAllForm'}) == None: # scrape homepage data
        scrape_home(soup)
    else: # output error message
        append_all((strftime("%Y-%m-%d %H:%M:%S", localtime())), homeArrays)
        append_all('ERROR:', homeArrays)
        append_all(soup.find('p',{'id':'ErrorNumber'}).text, homeArrays)
    
    # write homepage data to CSV
    write_to_csv(filePath, ',', assignedOnline, assignedOffline, 
        assignedInactive, unassigned, totalDealers)

except common.TimeoutException:
    traceback.print_exc()
    print('HOME PAGE REACHED MAX LOAD TIME OF 60 SECONDS. PLEASE CHECK:')
    print('  - YOUR NETWORK CONNECTION')
    print('  - THAT ' + driver.current_url + ' IS NOT UNDER MAINTENANCE\n')
    cursor.show()
    e = input('press \'Enter\' to exit or close this window.\n')
    if e != None:
        sys.exit()
except:
    traceback.print_exc()
    print('\nEXCEPTION CAUGHT WHILE SCRAPING HOME: ENSURE THAT THE LOGIN INFORMATION AND HOME PAGE URL IN PRIVATE.JSON ARE CORRECT\n')
    cursor.show()
    e = input('press \'Enter\' to exit or close this window.\n')
    if e != None:
        sys.exit()

try: # scrape unit data based on user input

    if i == '1': # get data from a random unit
        prog = 1.0
        total = 3.0

        # get a random mac
        mac = secrets.choice(macArray)

        # crawl the unit's pages
        crawl_unit(mac, driver)

    elif i == '2': # get data from all units
        prog = 1.0
        total = (len(macArray) * 2.0) + 1.0

        # crawl each unit's pages
        for x in macArray:
            mac = x
            crawl_unit(mac, driver)

    elif i == '3': # get data from a specific unit
        prog = 1.0
        total = 3.0

        # crawl the unit's pages
        crawl_unit(mac, driver)

    else: # invalid command line argument
        print('INVALID COMMAND LINE ARGUMENT: UNABLE TO DETERMINE WHICH UNITS TO SCRAPE')

except common.TimeoutException:
    traceback.print_exc()
    print('UNIT PAGE REACHED MAX LOAD TIME OF 60 SECONDS. PLEASE CHECK:')
    print('  - YOUR NETWORK CONNECTION')
    print('  - THAT THE UNIT PAGE FOR ' + mac + ' IS NOT UNDER MAINTENANCE AND IS FUNCTIONING PROPERLY')
    print('THEN RE-RUN THE APPLICATION\n')
    cursor.show()
    e = input('press \'Enter\' to exit or close this window.\n')
    if e != None:
        sys.exit()
except:
    traceback.print_exc()
    print('\nEXCEPTION CAUGHT WHILE SCRAPING UNIT')
    print('AT MAC ADDRESS: ' + mac)
    print('AT URL: ' + driver.current_url + '\n')
    cursor.show()
    e = input('press \'Enter\' to exit or close this window or close this window.\n')
    if e != None:
        sys.exit()

try:
    # close the webdriver
    driver.close()
except:
    traceback.print_exc()
    print('\nUNABLE TO CLOSE THE WEBDRIVER\n')

# print execution runtime
td = datetime.now() - kickoff
print('Execution took ' + str(td.total_seconds()) + ' seconds.')

# indicate completion
print('Complete.\n')

cursor.show()
sys.exit()
