# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 17:58:04 2017

@author: jol7019
"""

#<>  Pull in requisite python libraries
#<>----------------------------------------------------------
import pandas as pd


#<>  Pull in the instruction file
#<>----------------------------------------------------------
filelocation   = 'C:\Users\jol7019\Desktop\NOVICK'
FileIDForPull  = pd.read_csv(filelocation+'\NovickInstructionFilerID.csv',sep=',')
UniqueFilerID  = pd.Series(FileIDForPull.FilerID.unique())

#<>  Pull in the list of filerid from database
#<>----------------------------------------------------------


