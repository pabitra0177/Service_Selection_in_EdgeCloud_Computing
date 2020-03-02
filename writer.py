import sys
#import csv
import pandas
import numpy

file_h="taskHistory.csv"

#var.seek(0)

#data=pandas.read_csv(var,header=None)
data=pandas.read_csv(file_h)
print(data)
print(type(data))

''' 
#not required
data=data.values
print(data)
print(type(data))
'''


# copied ========================================

data=pandas.read_csv(file_h)
print(data)
d2={'device_count':0,'task_size':0,'Lan_Delay':0,'Server_Ut':0,'Failure_mob':0,'Exec_time':0,'Vm_ut':0,'failure_VmCap':0,'Decission':2}
data=data.append(d2,ignore_index=True)
print(data)

data.to_csv(file_h)