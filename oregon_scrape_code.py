# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


#--

import pandas as pd
import pyodbc
server   = 'novickdb2.database.windows.net'
database = 'NovickLuna'
username = 'novick123'
password = 'Philofsky123'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute('''SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName 
FROM [SalesLT].[ProductCategory] pc 
JOIN [SalesLT].[Product] p ON pc.productcategoryid = p.productcategoryid''')
row = cursor.fetchone()
while row:
    print (str(row[0]) + " " + str(row[1]))
    row = cursor.fetchone()

SQL = '''
CREATE TABLE BASETABLE
(
  Campus                        varchar(20) NOT NULL,  
  EagleUnitName                 varchar(20) NOT NULL, 
  SystemUnitEpiPortal           varchar(20) NOT NULL,
  SystemPatientTypeEpiPortal    varchar(20) NOT NULL,
  SystemUnitNameNHSN            varchar(20) NOT NULL, 
  SystemPatientTypeNHSN         varchar(20) NOT NULL,
  NHSNStartDate                 varchar(20) NOT NULL,
  NHSNEndDate                   varchar(20) NOT NULL, 
  
);'''

 
cursor.execute(SQL)
cursor.execute('select * from  BASETABLE')


query = '''
INSERT INTO BASETABLE (
      Campus,
      EagleUnitName   , 
      SystemUnitEpiPortal,
      SystemPatientTypeEpiPortal,
      SystemUnitNameNHSN, 
      SystemPatientTypeNHSN,
      NHSNStartDate,
      NHSNEndDate )
VALUES (
'1','2','3','4','5','6','7','8'
);

'''
cursor.execute(query)


cursor.execute('select * from  BASETABLE')

row = cursor.fetchone()


for(row in 1:NROW(NHSNXWalk)){
    query = 
      "INSERT INTO ##temp1 (
      Campus,
      EagleUnitName   , 
      SystemUnitEpiPortal,
      SystemPatientTypeEpiPortal,
      SystemUnitNameNHSN, 
      SystemPatientTypeNHSN,
      NHSNStartDate,
      NHSNEndDate )
      VALUES (
      '", NHSNXWalk$Campus[row],"', 
      '", NHSNXWalk$EagleUnitName[row],"', 
      '", NHSNXWalk$SystemUnitEpiPortal[row],"', 
      '", NHSNXWalk$SystemPatientTypeEpiPortal[row],"', 
      '", NHSNXWalk$SystemPatientTypeNHSN[row],"', 
      '", NHSNXWalk$SystemPatientTypeNHSN[row],"', 
      '", NHSNXWalk$NHSNStartDate[row],"', 
      '", NHSNXWalk$NHSNEndDate[row],"' 
      )"

row = cursor.fetchone()
while row:
    print (str(row[0]) + " " + str(row[1]))
    row = cursor.fetchone()

 
 

sqlQuery(cnxn,SQL)




