# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 11:28:36 2017

@author: jol7019
"""


#<>----------------------------------------------------------
#<>  [1]
#<>  Pull in requisite python libraries
#<>----------------------------------------------------------
import pandas as pd
import pyodbc
import scraperwiki
import mechanize
import re
from   datetime import date, timedelta, datetime
import xlrd


#<>----------------------------------------------------------
#<>  [2]
#<>  Pull in the instruction file
#<>----------------------------------------------------------
filelocation   = 'C:\Users\jol7019\Desktop\NOVICK'
FileIDForPull  = pd.read_csv(filelocation+'\NovickInstructionFilerID.csv',sep=',')
UniqueFilerID  = pd.DataFrame(pd.Series(FileIDForPull.FilerID.unique()), columns=['filerid'])

#<>----------------------------------------------------------
#<>  [3]  
#<>  Connect to Azure VM SQL database
#<>----------------------------------------------------------

server   = 'novickdb2.database.windows.net'
database = 'NovickLuna'
username = 'novick123'
password = 'Philofsky123'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#<>----------------------------------------------------------
#<>  [4]
#<>  Create relevant instructions for scraping in form of filerid
#<>----------------------------------------------------------

#sql command 1.  Drop 'INSTRUCT_FILERID' table
SQL = ''' if object_id('INSTRUCT_FILERID') is not null drop table INSTRUCT_FILERID;'''
cursor.execute(SQL)

#sql command 2.  Create 'INSTRUCT_FILERID' table
SQL = ('''CREATE TABLE INSTRUCT_FILERID
           (
                   FilerID     varchar(20) NOT NULL,   
       ''' +  
       ''');
       ''')
cursor.execute(SQL)
 
#sql command 3.  Insert data into table: 'INSTRUCT_FILERID'
for i in range(0,len(UniqueFilerID)): 
    SQL = ('''
           INSERT INTO INSTRUCT_FILERID ( 
                   FilerID
                   )  
           VALUES (  ''' + 
                   str(UniqueFilerID['filerid'].iloc[i]) +
            ''');
            '''
    )
    cursor.execute(SQL)        





