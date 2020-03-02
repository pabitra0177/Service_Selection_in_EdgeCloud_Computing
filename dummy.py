import sys
import math

def probability_calc(x): # left eq and right eq
    x=x/100
    if x>0.40 and x<0.50:
        t2=(-5)*(x-0.4)+1
        t2=float(t2)
        t2=round(t2,3)
        t3=1-t2
        t3=round(t3,3)

    elif x>0.50 and x<0.60: 
        t3=5*(x-0.4)
        t3=float(t3)
        t3=round(t3,3)
        t2=1-t3
        t2=round(t2,3)

    elif x<=0.40:
        t2=1
        t3=0

    else:
        t2=0
        t3=1
    
    return [t2*100,t3*100]




def dummy_outputs(task,tier):
    '''
    task[0] = 
    task[1] = 
    task[2] = 
    task[3] = 
    '''
    op_time=[]
    
    pass