# Wripli Crawler
**_This program is designed to streamline the testing process and improve decision-making as it relates to the user experience of Wripli._**
****
## VERSION 1.4
  - Implemented 60 second webdriver timeout
  - Improved exception outputs
  - Improved outputs for unpopulated fields
  - Improved code style and concision
  - Fixed AttributeError bug
  
## VERSION 1.3
  - Implemented private.json config file
  - Implemented ability to crawl consumer page
  - Improved exception handling
  - Improved UI
  - Fixed bugs

## VERSION 1.2: 
  - Implemented ability to pull data from one, all, or a random unit
  - Implemented ability to pass command line arguments
  - Made dataset file path flexible
  - Implemented datasheet reset functionality within dealer-crawler.py
  - Improved UI
  
## VERSION 1.1: 
  - Removed all prior commit history, creating a safe production version of WripliCrawler.
****
## How to use:
  1. Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  2. Install [Python](https://www.python.org/downloads/release/python-3105/)
  3. Install [pip](https://pip.pypa.io/en/stable/installation/)
  3. Install [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/#installing-beautiful-soup)
  4. Install [Firefox](https://www.mozilla.org/en-US/firefox/new/)
  5. Install [GeckoDriver](https://github.com/mozilla/geckodriver/releases) (don't forget to `pip install webdriver_manager`)
  6. Install [Selenium](https://selenium-python.readthedocs.io/installation.html)
  7. Click **USE THIS TEMPLATE** and create your new repository
  8. Edit private_TEMPLATE.json per your desired result
  9. Rename to private.json (consider placing in same directory and using .gitignore to avoid compromising privacy)
  10. Run
  11. If you wish to schedule it to run at prescribed times, see [this site](https://desktop.arcgis.com/en/arcmap/10.7/analyze/python/scheduling-a-python-script-to-run-at-prescribed-times.htm) and be sure to pass [appropriate command-line arguments](https://github.com/ttbauer4/WripliCrawler/issues/5#issuecomment-1198194970).
  12. If you wish to package your crawler into an executable file, use [PyInstaller](https://pyinstaller.org/en/stable/)
