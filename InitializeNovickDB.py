# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 23:30:55 2017

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
#<>  [3]  
#<>  Pull the needed filerid for review
#<>----------------------------------------------------------
SQL = 'select  FilerID from INSTRUCT_FILERID;'
FilerIDCheckList = pd.read_sql(SQL, cnxn)
FilerIDCheckList = pd.Series(FilerIDCheckList.FilerID.unique())

#<>----------------------------------------------------------
#<>  [4]  
#<>  Scrape
#<>----------------------------------------------------------
currentdate = date.today()
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_robots(False)
data = []


for j in range(0,len(FilerIDCheckList)):
    print("( " + str(j+1)+" of " +str(len(FilerIDCheckList)) +" )") 
    for i in range(0,5):
       
        url = 'https://secure.sos.state.or.us/orestar/cneSearch.do?cneSearchButtonName=search&cneSearchFilerCommitteeId='+ str(FilerIDCheckList[j])
        #url = 'https://secure.sos.state.or.us/orestar/gotoPublicTransactionSearchResults.do?cneSearchButtonName=search&cneSearchFilerCommitteeId=*&cneSearchTranEndDate=' + date.strftime(currentdate, '%m/%d/%Y') + '&cneSearchTranStartDate=' + date.strftime(currentdate - timedelta(days=7), '%m/%d/%Y')
        print url
        br.open(url)
        xlsLink = br.follow_link(text_regex=r"Export To Excel Format")
        book = xlrd.open_workbook(file_contents=xlsLink.read())
        filings = book.sheet_by_index(0)
        for row in range(1, filings.nrows):
            datum = {
                "transaction_id" : filings.cell(row, 0).value,
                "original_id" : filings.cell(row, 1).value,
                "tran_date" : filings.cell(row, 2).value,
                "tran_status" : filings.cell(row, 3).value,
                "filer" : filings.cell(row, 4).value,
                "payee" : filings.cell(row, 5).value,
                "sub_type" : filings.cell(row, 6).value,
                "amount" : filings.cell(row, 7).value,
                "aggregate_amount" : filings.cell(row, 8).value,
                "payee_committe" : filings.cell(row, 9).value,
                "filer_id" : filings.cell(row, 10).value,
                "attest_by_name" : filings.cell(row, 11).value,
                "attest_date" : filings.cell(row, 12).value,
                "review_by_name" : filings.cell(row, 13).value,
                "review_date" : filings.cell(row, 14).value,
                "due_date" : filings.cell(row, 15).value,
                "occpn_ltr_date" : filings.cell(row, 16).value,
                "pymt_sched_txt" : filings.cell(row, 17).value,
                "purpose_description" : filings.cell(row, 18).value,
                "interest_rate" : filings.cell(row, 19).value,
                "check_number" : filings.cell(row, 20).value,
                "tran_stsfd_ind" : filings.cell(row, 21).value,
                "filed_by_name" : filings.cell(row, 22).value,
                "filed_date" : filings.cell(row, 23).value,
                "addr_book_agent_name" : filings.cell(row, 24).value,
                "book_type" : filings.cell(row, 25).value,
                "title_text" : filings.cell(row, 26).value,
                "occupation_text" : filings.cell(row, 27).value,
                "employer_name" : filings.cell(row, 28).value,
                "employer_city" : filings.cell(row, 29).value,
                "employer_state" : filings.cell(row, 30).value,
                "employer_ind" : filings.cell(row, 31).value,
                "self_employed" : filings.cell(row, 32).value,
                "addr_line_1" : filings.cell(row, 33).value,
                "addr_line_2" : filings.cell(row, 34).value,
                "city" : filings.cell(row, 35).value,
                "state" : filings.cell(row, 36).value,
                "zip" : filings.cell(row, 37).value,
                "zip_plus_4" : filings.cell(row, 38).value,
                "county" : filings.cell(row, 39).value,
                "purpose_codes" : filings.cell(row, 40).value,
                "exp_date" : filings.cell(row, 41).value
            }
            data.append(datum)
     #   currentdate = currentdate - timedelta(days=7)
        scraperwiki.sqlite.save(["transaction_id"], data)

AllFilerIDScrape = pd.DataFrame(data)   
AllFilerIDScrape = AllFilerIDScrape[['transaction_id',
'original_id','tran_date','tran_status','filer',
'payee','sub_type','amount','aggregate_amount',
'payee_committe','filer_id','attest_by_name','attest_date',
'review_by_name','review_date','due_date','occpn_ltr_date',
'pymt_sched_txt','purpose_description','interest_rate',
'check_number','tran_stsfd_ind','filed_by_name','filed_date',
'addr_book_agent_name','book_type','title_text','occupation_text',
'employer_name','employer_city','employer_state','employer_ind','self_employed',
'addr_line_1','addr_line_2','city','state','zip','zip_plus_4',
'county','purpose_codes','exp_date'
]]

AllFilerIDScrape['scrape_date'] = str(currentdate)

AllFilerIDScrape['payee'] = AllFilerIDScrape.payee.str.replace("'","")
AllFilerIDScrape['payee'] = AllFilerIDScrape['payee'].str[:2000]
AllFilerIDScrape['employer_name'] = AllFilerIDScrape.employer_name.str.replace("'","")
AllFilerIDScrape['employer_name'] = AllFilerIDScrape['employer_name'].str[:2000]
AllFilerIDScrape['purpose_codes'] = AllFilerIDScrape.purpose_codes.str.replace("'","")
AllFilerIDScrape['purpose_codes'] = AllFilerIDScrape['purpose_codes'].str[:2000]
AllFilerIDScrape['occupation_text'] = AllFilerIDScrape.occupation_text.str.replace("'","")
AllFilerIDScrape['occupation_text'] = AllFilerIDScrape['occupation_text'].str[:2000]
AllFilerIDScrape['title_text'] = AllFilerIDScrape.title_text.str.replace("'","")
AllFilerIDScrape['title_text'] = AllFilerIDScrape['title_text'].str[:2000]
AllFilerIDScrape['filer'] = AllFilerIDScrape.filer.str.replace("'","")
AllFilerIDScrape['filer'] = AllFilerIDScrape['filer'].str[:2000]
AllFilerIDScrape['book_type'] = AllFilerIDScrape.book_type.str.replace("'","")
AllFilerIDScrape['book_type'] = AllFilerIDScrape['book_type'].str[:2000]
AllFilerIDScrape['sub_type'] = AllFilerIDScrape.sub_type.str.replace("'","")
AllFilerIDScrape['sub_type'] = AllFilerIDScrape['sub_type'].str[:2000]
AllFilerIDScrape['payee_committe'] = AllFilerIDScrape['payee_committe'].astype(str) 
AllFilerIDScrape['payee_committe'] = AllFilerIDScrape.payee_committe.str.replace("'","")
AllFilerIDScrape['payee_committe'] = AllFilerIDScrape['payee_committe'].str[:2000]
AllFilerIDScrape['attest_by_name'] = AllFilerIDScrape.attest_by_name.str.replace("'","")
AllFilerIDScrape['attest_by_name'] = AllFilerIDScrape['attest_by_name'].str[:2000]
AllFilerIDScrape['review_by_name'] = AllFilerIDScrape.review_by_name.str.replace("'","")
AllFilerIDScrape['review_by_name'] = AllFilerIDScrape['review_by_name'].str[:2000]
AllFilerIDScrape['pymt_sched_txt'] = AllFilerIDScrape.pymt_sched_txt.str.replace("'","")
AllFilerIDScrape['pymt_sched_txt'] = AllFilerIDScrape['pymt_sched_txt'].str[:2000]
AllFilerIDScrape['purpose_description'] = AllFilerIDScrape.purpose_description.str.replace("'","")
AllFilerIDScrape['purpose_description'] = AllFilerIDScrape['purpose_description'].str[:2000]
AllFilerIDScrape['filed_by_name'] = AllFilerIDScrape.filed_by_name.str.replace("'","")
AllFilerIDScrape['filed_by_name'] = AllFilerIDScrape['filed_by_name'].str[:2000]
AllFilerIDScrape['addr_book_agent_name'] = AllFilerIDScrape['addr_book_agent_name'].astype(str)
AllFilerIDScrape['addr_book_agent_name'] = AllFilerIDScrape.addr_book_agent_name.str.replace("'","")
AllFilerIDScrape['addr_book_agent_name'] = AllFilerIDScrape['addr_book_agent_name'].str[:2000]
AllFilerIDScrape['addr_line_1'] = AllFilerIDScrape.addr_line_1.str.replace("'","")
AllFilerIDScrape['addr_line_1'] = AllFilerIDScrape['addr_line_1'].str[:2000]
AllFilerIDScrape['addr_line_2'] = AllFilerIDScrape.addr_line_2.str.replace("'","")
AllFilerIDScrape['addr_line_2'] = AllFilerIDScrape['addr_line_2'].str[:2000]
AllFilerIDScrape['city'] = AllFilerIDScrape.city.str.replace("'","")
AllFilerIDScrape['city'] = AllFilerIDScrape['city'].str[:2000]


#AllFilerIDScrape.to_csv('FullyScrapedOregon.csv')

AllFilerIDScrape = pd.read_csv('FullyScrapedOregon.csv')
#x=AllFilerIDScrape
#<>----------------------------------------------------------
#<>  [5]  
#<>  Push to Azure VM SQL Server
#<>----------------------------------------------------------

server   = 'novickdb2.database.windows.net'
database = 'NovickLuna'
username = 'novick123'
password = 'Philofsky123'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

cursor.execute("CREATE SCHEMA ORESTAR  ;")  

#sql command 1.  Drop 'FilerData' table
SQL = ''' if object_id('ORESTAR.FilerDB') is not null drop table ORESTAR.FilerDB;'''
cursor.execute(SQL)



#sql command 2.  Create 'INSTRUCT_FILERID' table
SQL = ('''CREATE TABLE ORESTAR.FilerDB
           (
                 transaction_id     varchar(2000),
original_id     varchar(2000),
tran_date     varchar(2000),
tran_status     varchar(2000),
filer     varchar(2000),
payee     varchar(2000),
sub_type     varchar(2000),
amount     varchar(2000),
aggregate_amount     varchar(2000),
payee_committe     varchar(2000),
filer_id     varchar(2000),
attest_by_name     varchar(2000),
attest_date     varchar(2000),
review_by_name     varchar(2000),
review_date     varchar(2000),
due_date     varchar(2000),
occpn_ltr_date     varchar(2000),
pymt_sched_txt     varchar(2000),
purpose_description     varchar(2000),
interest_rate     varchar(2000),
check_number     varchar(2000),
tran_stsfd_ind     varchar(2000),
filed_by_name     varchar(2000),
filed_date     varchar(2000),
addr_book_agent_name     varchar(2000),
book_type     varchar(2000),
title_text     varchar(2000),
occupation_text     varchar(2000),
employer_name     varchar(2000),
employer_city     varchar(2000),
employer_state     varchar(2000),
employer_ind     varchar(2000),
self_employed     varchar(2000),
addr_line_1     varchar(2000),
addr_line_2     varchar(2000),
city     varchar(2000),
state     varchar(2000),
zip     varchar(2000),
zip_plus_4     varchar(2000),
county     varchar(2000),
purpose_codes     varchar(2000),
exp_date     varchar(2000),
scrape_date    varchar(2000)
       ''' +  
       ''');
       ''')
cursor.execute(SQL)
 
#sql command 3.  Insert data into table: 'INSTRUCT_FILERID'
for i in range(18,len(AllFilerIDScrape)): 
    print("( " + str(i+1)+" of " +str(len(AllFilerIDScrape)) +" )") 
    SQL = ('''
           INSERT INTO ORESTAR.FilerDB ( 
                   transaction_id,
original_id,
tran_date,
tran_status,
filer,
payee,
sub_type,
amount,
aggregate_amount,
payee_committe,
filer_id,
attest_by_name,
attest_date,
review_by_name,
review_date,
due_date,
occpn_ltr_date,
pymt_sched_txt,
purpose_description,
interest_rate,
check_number,
tran_stsfd_ind,
filed_by_name,
filed_date,
addr_book_agent_name,
book_type,
title_text,
occupation_text,
employer_name,
employer_city,
employer_state,
employer_ind,
self_employed,
addr_line_1,
addr_line_2,
city,
state,
zip,
zip_plus_4,
county,
purpose_codes,
exp_date,
scrape_date
                   )  
           VALUES (  ''' + 
"'" +str(AllFilerIDScrape['transaction_id'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['original_id'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['tran_date'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['tran_status'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['filer'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['payee'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['sub_type'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['amount'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['aggregate_amount'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['payee_committe'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['filer_id'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['attest_by_name'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['attest_date'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['review_by_name'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['review_date'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['due_date'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['occpn_ltr_date'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['pymt_sched_txt'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['purpose_description'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['interest_rate'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['check_number'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['tran_stsfd_ind'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['filed_by_name'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['filed_date'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['addr_book_agent_name'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['book_type'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['title_text'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['occupation_text'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['employer_name'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['employer_city'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['employer_state'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['employer_ind'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['self_employed'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['addr_line_1'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['addr_line_2'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['city'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['state'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['zip'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['zip_plus_4'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['county'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['purpose_codes'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['exp_date'].iloc[i]) + "'" + ',' +
"'" +str(AllFilerIDScrape['scrape_date'].iloc[i]) + "'" +

            ''');
            '''
    )
    cursor.execute(SQL)       

  

CREATE SCHEMA [DB] AUTHORIZATION [dbo]

pd.read_sql("select * from NocvickLuna.FilerDB",cnxn)

pd.read_sql("SELECT * FROM sys.Tables", cnxn)


pd.read_sql("SELECT * FROM sys.Tables", cnxn)

