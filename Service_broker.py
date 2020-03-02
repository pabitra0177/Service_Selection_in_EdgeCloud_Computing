import sys
import math


sla_delay=49.6
sla_failure_due_to_mobility=8
tolerance_factor=1
#tolerance_factor=1.05

def sla_comparator(task): # task is a list
    sla_score=4

    if task[0]<=1200:
        sla_score-=1
    if task[1]<180000:
        sla_score-=1
    if task[2]<=0.496:
        sla_score-=1
    if task[3]<9:
        sla_score-=1

    return sla_score



'''
In the function 
dec is a string 
"22","23","32","33"
'''
'''
task[0] = device count
task[1] = no of tasks
task[2] = delay
task[3] = mobility fail 
'''