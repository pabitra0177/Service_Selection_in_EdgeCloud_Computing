import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


#class RuleBook:

device_count=ctrl.Antecedent(np.arange(200,2000,1), 'device_count')
no_of_task = ctrl.Antecedent(np.arange(50000, 320000, 1000), 'no_of_task')
LAN_delay = ctrl.Antecedent(np.arange(40,69,0.5), 'LAN_delay')
mobility_failure = ctrl.Antecedent(np.arange(1, 38, 0.5), 'mobility_failure')

architecture = ctrl.Consequent(np.arange(0, 100, 1), 'architecture')

device_count['low']=fuzz.trapmf(device_count.universe,[0,0,1100,1300])
device_count['high']=fuzz.trapmf(device_count.universe,[1100,1300,2000,2000])

no_of_task['low']=fuzz.trapmf(no_of_task.universe,[50000,50000,100000,130000]) 
no_of_task['high']=fuzz.trapmf(no_of_task.universe,[100000,130000,320000,320000])

LAN_delay['low'] = fuzz.trapmf(LAN_delay.universe, [0, 0, 46, 52])
LAN_delay['high'] = fuzz.trapmf(LAN_delay.universe, [46, 52,70, 70])

mobility_failure['low'] = fuzz.trapmf(mobility_failure.universe, [0, 0, 7, 9])
mobility_failure['high'] = fuzz.trapmf(mobility_failure.universe, [7,9,38,38])


'''
device_count.view()
no_of_task.view()
LAN_delay.view()
mobility_failure.view()
'''

architecture['2tier'] = fuzz.trapmf(architecture.universe, [0,0, 40, 60])
architecture['3tier'] = fuzz.trapmf(architecture.universe, [40,60, 100, 100])

'''
architecture.view()
'''
#Rule

rule11=ctrl.Rule(device_count['low'],architecture['2tier'])
rule12=ctrl.Rule(device_count['high'],architecture['3tier'])

rule31 = ctrl.Rule(LAN_delay['low'], architecture['2tier'])
rule32 = ctrl.Rule(LAN_delay['high'] , architecture['3tier'])

rule22 = ctrl.Rule(mobility_failure['high'] , architecture['3tier'])
rule21 = ctrl.Rule(mobility_failure['low'] ,architecture['2tier'])

rule42=ctrl.Rule(no_of_task['high'],architecture['3tier'])
rule41=ctrl.Rule(no_of_task['low'],architecture['2tier'])


architecturing_ctrl = ctrl.ControlSystem(rules = [ rule21,rule22, rule31,rule32,rule41,rule42,rule11,rule12,])    
architecturing = ctrl.ControlSystemSimulation(architecturing_ctrl)

architecturing.input['device_count']=1600 #2
architecturing.input['no_of_task']=110256 #2 
architecturing.input['LAN_delay'] = 60   #3
architecturing.input['mobility_failure'] = 16.8 #3

# Crunch the numbers
architecturing.compute()
print(architecturing.output['architecture'])

output=architecturing.output['architecture']

if(output>50):
	print("Edge Should be introduced")
else:
	print("Edge should not be introduced")




plt.show()
