import sys
import numpy
import scipy.interpolate as gf
interpolate = gf.interp1d

No_of_Devices=numpy.arange(200,2001,200)
Latency=[40,42.1,44.2,46.9,49,52.5,56.5,59.8,63,66.4]
Mob_Failure=[3,6,9.5,11.5,15,18,22,24,26.5,28.5]
No_of_Tasks=[48253,93747,142574,183808,232514,273028,324661,368472,413739,479459]


#linear
l_linear=interpolate(No_of_Devices,Latency,kind='linear')
f_linear=interpolate(No_of_Devices,Mob_Failure,kind='linear')
t_linear=interpolate(No_of_Devices,No_of_Tasks,kind='linear')

#narest
l_nearest=interpolate(No_of_Devices,Latency,kind='nearest')
f_nearest=interpolate(No_of_Devices,Mob_Failure,kind='nearest')
t_nearest=interpolate(No_of_Devices,No_of_Tasks,kind='nearest')

#slinear
l_slinear=interpolate(No_of_Devices,Latency,kind='slinear')
f_slinear=interpolate(No_of_Devices,Mob_Failure,kind='slinear')
t_slinear=interpolate(No_of_Devices,No_of_Tasks,kind='slinear')

#print(t_linear(1251))