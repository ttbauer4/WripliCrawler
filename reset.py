#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' reset.py: resets datasheet
'''

__author__ = 'Trenton Bauer'
__version__ = 'V1.1'
__maintainer__ = 'Trenton Bauer'
__contact__ = 'trenton.bauer@gmail.com'
__status__ = 'Prototype'

import os
import private

# remove existing file
if (os.path.exists(private.wdFileName) and os.path.isfile(private.wdFileName)):
    os.remove(private.wdFileName)
    print('file deleted')
else:
    print('file not found')

# create new file with headers
file = open(private.wdFileName, 'w')
file.write('TIMESTAMP,MAC ADDRESS,UNIT NAME,FIELD,VALUE\n')
print(private.wdFileName + ' created')
file.close()