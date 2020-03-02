import sys
import os
import numpy
import pandas
import csv

historyFile="taskHistory.csv" # name of the csv file storing TaskHistory

class History:

    def reader(self,file_r,selection_list): # to read history for csv,xlsx files only
         
        # selection list is the list that contains the parameters of ip Data
        # ['no_of_tasks','Lan_delay','Failure_mob']
        data=pandas.read_csv(file_r) # for csv
        #data=pandas.read_excel(file_r) # for xlsx
        ip_data=data[selection_list]
        
        #print(ip_data)
        #print(type(ip_data))

        return data,ip_data

    def writer(self,record,file): # to update the history
        with open(file,'a',newline='')  as var:
            #var.seek(0)
            write=csv.writer(var)
            write.writerow(record) #<<<<<<<=========
            var.close()
        



    