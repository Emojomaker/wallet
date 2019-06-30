"""Module for logging operations to log file"""

import datetime

def log(message):
    """Creating/opening log file and write operation message"""
    date = datetime.datetime.now()
    with open('log_operations', 'a') as file:
        file.write(str(date)+': '+ str(message)+'\n')
