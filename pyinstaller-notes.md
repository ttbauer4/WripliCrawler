## INSTALLATION OF UNIX EXECUTABLE FILE:
1. open Terminal
2. navigate to your project directory
3. execute the following command: 
    - ```pyi-makespec dealer-crawler.py --add-data private.json:. --add-data WripliData.csv:. --add-binary driver/geckodriver:driver/ --name dealer-crawler```
4. open dealer-crawler.spec
5. paste the following at the bottom:
    - ```import shutil```
    - ```shutil.copyfile('private.json', '{0}/private.json'.format(DISTPATH))```
    - ```shutil.copyfile('WripliData.csv', '{0}/WripliData.csv'.format(DISTPATH))```
6. execute the following command in Terminal: 
    - ```pyinstaller --clean dealer-crawler.spec```
7. /dist/private.json and /dist/WripliData.csv may be deleted, but /dist/dealer-crawler/private.json and WripliData.csv should be kept

## INSTALLATION OF WINDOWS EXECUTABLE FILE:
1. open Command Prompt
2. navigate to your project directory
3. execute the following command:
   - ```pyi-makespec dealer-crawler.py --add-data private.json;. --add-data WripliData.csv;. --add-binary driver/geckodriver.exe;driver/ --name dealer-crawler```
4. open dealer-crawler.spec
5. paste the following at the bottom:
    - ```import shutil```
    - ```shutil.copyfile('private.json', '{0}/private.json'.format(DISTPATH))```
    - ```shutil.copyfile('WripliData.csv', '{0}/WripliData.csv'.format(DISTPATH))```
6. execute the following command in Command Prompt: 
    - ```pyinstaller --clean dealer-crawler.spec```
7. /dist/private.json and /dist/WripliData.csv may be deleted, but /dist/dealer-crawler/private.json and WripliData.csv should be kept
