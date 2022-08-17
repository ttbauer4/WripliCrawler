## INSTALLATION OF UNIX EXECUTABLE FILE:
 1. open Terminal
 2. navigate to the directory of your .py file
 3. execute the following command: ```pyi-makespec dealer-crawler.py --add-data private.json:. --add-data WripliData.csv:. --add-binary driver/geckodriver:driver/ --name dealer-crawler```
 4. open dealer-crawler.spec
 5. paste the following at the bottom:
        ```import shutil```
        ```shutil.copyfile('private.json', '{0}/private.json'.format(DISTPATH))```
        ```shutil.copyfile('WripliData.csv', '{0}/WripliData.csv'.format(DISTPATH))```
6. execute the following command in Terminal: ```pyinstaller --clean dealer-crawler.spec``