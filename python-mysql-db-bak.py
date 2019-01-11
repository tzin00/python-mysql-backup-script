#!/usr/bin/python

###########################################################
#
# This python script is used for mysql database backup
# using mysqldump and tar utility.
#
# Written by : Thant Zin Oo
# Company Name: BRYCEN Myanmar
# Created date: Dec 12, 2018
# Last modified: Dec 19, 2018
# Tested with : Python 2.7.15
# Script Revision: 2.5
#
##########################################################

# Import required python libraries
import os
from datetime import datetime
import time
import pipes
import shutil


# Global variable for generating time stamp
logfile = "/home/db_bak/db_bak.log"
DB_HOST = 'localhost'
DB_USER = 'user'
DB_USER_PASSWORD = 'P@s5w0Rd'
DB_NAME = '/root/dbnameslist.txt'
#DB_NAME = 'velbon'
BACKUP_PATH = '/home/db_bak/'

def logging_file(message):
    time_now = time.strftime("%Y/%m/%d - %H:%M:%S")
    # Logging backup transaction
    file = open(logfile, 'a')
    file.write(time_now + ' - ' + str(message) + '\n')
    file.close()

today_date = time.strftime('%Y%m%d-%H%M%S')
TODAYBACKUPPATH = BACKUP_PATH + '/' + today_date
# Checking if backup folder already exists or not. If not exists will create it.
try:
    os.stat(TODAYBACKUPPATH)
except:
    os.mkdir(TODAYBACKUPPATH)

def check_db_file():
    #Global variable
    global DB_NAME
    if os.path.exists(DB_NAME):
        file1 = open(DB_NAME)
        multi = 1
        # Logging backup transaction
        logging_file(message='Databases file found...')
        logging_file(message='Starting backup of all dbs listed in file ({})'.format(DB_NAME))
    else:
        # Logging backup transaction
        logging_file(message='Databases file not found...')
        logging_file(message='Starting backup of database named ({})'.format(DB_NAME))
        multi = 0
    return multi

def db_backup_proc():
    #Global variable
    global DB_NAME, DB_HOST, DB_USER, DB_USER_PASSWORD, BACKUP_PATH, TODAYBACKUPPATH
    # Starting actual database backup process.
    check_db_result = check_db_file()
    if check_db_result:
       in_file = open(DB_NAME,"r")
       flength = len(in_file.readlines())
       in_file.close()
       p = 1
       dbfile = open(DB_NAME,"r")

       while p <= flength:
           db = dbfile.readline()   # reading database name from file
           db = db[:-1]         # deletes extra line
           dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
           os.system(dumpcmd)
           gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
           os.system(gzipcmd)
           # Logging backup transaction
           logging_file(message='Database named ({}) has been backup.'.format(db))
           p = p + 1
       dbfile.close()
    else:
       db = DB_NAME
       dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       os.system(dumpcmd)
       gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       os.system(gzipcmd)
       # Logging backup transaction
       logging_file(message='Database named ({}) has been backup.'.format(db))

def del_backup():
        global BACKUP_PATH
        current_cwd = os.listdir(BACKUP_PATH)
        current_cwd.sort()
        del_folder_name = current_cwd[:-4]
        for x in del_folder_name:
            shutil.rmtree(BACKUP_PATH + x)
            logging_file(message='Deleted old backup folder named ({})'.format(x))

db_backup_proc()
del_backup()
