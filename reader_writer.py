import sys
import csv
import pandas
import numpy

file="taskHistory.csv"
#var=open(file,'r')
#var.seek(0)

#data=pandas.read_csv(var,header=None)
var=file
data=pandas.read_csv(var)
print(data)
print(type(data))

data=data.values
print(data)
print(type(data))


#var.close()
#working
#======================

with open(file,'a',newline='')  as var:
    #var.seek(0)
    writer=csv.writer(var)
    
    writer.writerow([0,1,0,0,0,1,1,2,2])

var.close()

#working 
#================================
