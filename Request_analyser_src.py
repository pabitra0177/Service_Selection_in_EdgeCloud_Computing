import history_src 
from history_src import History
import interpolation
import dummy # comment later

import sys
import math
import random
import numpy
import random

import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt



class Request_analyser(History):

    #default block / threshold block
    # stores the threshold values
    # default weightage to cloud (2 tier)
    default_deviceCount=1200-1  #Range (200-2000)
    #default_taskSize=0         #Range(40000,520000)  #no default
    default_Landelay=49.6       #Range(40,69)
    default_failedMob=8        #Range(1-38)
    
        
    def rms(self,data,task): #takes a dataframe returns the rms array
        
        #operate on a copy
        df=data.copy()
        rows=df.shape[0] # finds the number of entries
        
        #intial condition
        if rows==0:
            return []

        #adds rms col
        rms=[0.0]*rows
        df['rms']=rms
        
        #df['device_count']=df['device_count']-task[0]
        df['no_of_tasks']=df['no_of_tasks']-task[1]
        df['Lan_delay']=df['Lan_delay']-task[2]
        df['Failure_mob']=df['Failure_mob']-task[3]

        df['rms']=df['no_of_tasks']**2 +df['Lan_delay']**2 +df['Failure_mob']**2
        df['rms']=df['rms']/rows

        rms=df['rms']
        rms=list(rms)
        rms=[ math.sqrt(a) for a in rms ]
        rms=[ round(a,5) for a in rms ]
        
        return rms
    
    def nearest_match(self,rms,df): # returns the index of the nearest match

        l=len(rms)
        if(l<2):
            return 0,2
        
        id=0
        min_val=min(rms)
        for i in range(1,l):
            if rms[i]==min_val:
                id=i
                break
        
        tier=df['Decision']
        tier=list(tier)
        dec1=tier[id]

        return id,dec1

    def fuzzy(self,task):

        device_count=ctrl.Antecedent(numpy.arange(200,2000,1), 'device_count')
        no_of_task = ctrl.Antecedent(numpy.arange(50000, 520000, 1000), 'no_of_task')
        LAN_delay = ctrl.Antecedent(numpy.arange(40,69,0.5), 'LAN_delay')
        mobility_failure = ctrl.Antecedent(numpy.arange(1, 35, 0.5), 'mobility_failure')

        architecture = ctrl.Consequent(numpy.arange(0, 100, 1), 'architecture')

        device_count['low']=fuzz.trapmf(device_count.universe,[0,0,1100,1300])
        device_count['high']=fuzz.trapmf(device_count.universe,[1100,1300,2000,2000])

        no_of_task['low']=fuzz.trapmf(no_of_task.universe,[50000,50000,269000,312000]) 
        no_of_task['high']=fuzz.trapmf(no_of_task.universe,[269000,312000,520000,520000])

        LAN_delay['low'] = fuzz.trapmf(LAN_delay.universe, [0, 0, 47, 53])
        LAN_delay['high'] = fuzz.trapmf(LAN_delay.universe, [47, 53,70, 70])

        mobility_failure['low'] = fuzz.trapmf(mobility_failure.universe, [0, 0, 7, 10])
        mobility_failure['high'] = fuzz.trapmf(mobility_failure.universe, [7,10,35,35])

        
        device_count.view()        
        no_of_task.view()
        LAN_delay.view()
        
        mobility_failure.view()
        
        
        architecture['2tier'] = fuzz.trapmf(architecture.universe, [0,0, 40, 60])
        architecture['3tier'] = fuzz.trapmf(architecture.universe, [40,60, 100, 100])
        
        architecture.view()
        plt.show()
        
        rule11=ctrl.Rule(device_count['low'],architecture['2tier'])
        rule12=ctrl.Rule(device_count['high'],architecture['3tier'])

        rule31 = ctrl.Rule(LAN_delay['low'], architecture['2tier'])
        rule32 = ctrl.Rule(LAN_delay['high'] , architecture['3tier'])

        rule22 = ctrl.Rule(mobility_failure['high'] , architecture['3tier'])
        rule21 = ctrl.Rule(mobility_failure['low'] ,architecture['2tier'])

        rule42=ctrl.Rule(no_of_task['high'],architecture['3tier'])
        rule41=ctrl.Rule(no_of_task['low'],architecture['2tier'])

        architecturing_ctrl = ctrl.ControlSystem(rules = [rule21,rule22, rule31,rule32,rule41,rule42,rule11,rule12,])    
        architecturing = ctrl.ControlSystemSimulation(architecturing_ctrl)

        architecturing.input['device_count']=task[0]
        architecturing.input['no_of_task']=task[1] 
        architecturing.input['LAN_delay'] =task[2]
        architecturing.input['mobility_failure'] = task[3]
        
        architecturing.compute()
        output=architecturing.output['architecture']

        return output


    def runner(self): #prepares the task list
        ''' 
        takes input of the task properties
        returns a list/tuple containing all the properties of a task
        # properties of a task come from a simulator, which are nothing but probable and expected values 
        # of some certain attributes
        ''' 
        task_i=[]
        # these are expected values for the packet
        # we do selection to optimize
        device_count=input("Enter the expected number of devices in the network(200-2000)  ")
        if device_count=='':
            device_count=self.default_deviceCount
        else:
            device_count=int(device_count)
        if device_count<200:
            device_count=200
        elif device_count>2000:
            device_count=2000-1
        task_i.append(device_count)

        no_of_tasks=float(input('Enter the no_of_tasks 45k-510k ')) # compulsory no default
        if no_of_tasks<40000:
            no_of_tasks=40000
        elif no_of_tasks>526000:
                no_of_tasks=526000

        task_i.append(no_of_tasks)

        delay=input("What is the expected delay:-  ")
        if delay=='':#blank
            delay=self.default_Landelay
        else:
            delay=float(delay)
        task_i.append(delay)


        mob_failure=input("What is expected failure due to mobility (4-35)")
        if mob_failure=='':
            mob_failure=self.default_failedMob
        else:
            mob_failure=float(mob_failure)
        if mob_failure>35:
            mob_failure=35
        task_i.append(mob_failure)


        #task_i=tuple(task_i)
        return task_i 

    def runner_interpolate(self):
        tasks=[] #a list of tasks
        
        check='123'
        choice=''
        print("kind of interpolation")
        print("1) for linear")
        print("2) for nearest")
        print("3) for slinear")
        choice=input("Enter ")

        random.seed()
        for  i in range(0,1000):
            task_i=[]
            
            count_device=random.randint(200,2000) ################################################
            
            if choice=='1':
                task_count=int(interpolation.t_linear(count_device))
                delay=float(interpolation.l_linear(count_device))
                delay=round(delay,3)
                mob_fail=float(interpolation.f_linear(count_device))
                mob_fail=round(mob_fail,3)

            elif choice=='2':
                task_count=int(interpolation.t_nearest(count_device))
                delay=float(interpolation.l_nearest(count_device))
                delay=round(delay,3)
                mob_fail=float(interpolation.f_nearest(count_device))
                mob_fail=round(mob_fail,3)

            elif choice=='3':
                task_count=int(interpolation.t_slinear(count_device))
                delay=float(interpolation.l_slinear(count_device))
                delay=round(delay,3)
                mob_fail=float(interpolation.f_slinear(count_device))
                mob_fail=round(mob_fail,3)

            else:
                pass

            task_i.append(count_device)
            task_i.append(task_count)
            task_i.append(delay)
            task_i.append(mob_fail)
            #print(task_i)
            tasks.append(task_i)
        
        return tasks        


    def main(self,task): # main scheduler

        #task scheduler
        self.task=task

        #History reading
        # selection list is the list that contains the parameters of ip Data
        selection_list=['no_of_tasks','Lan_delay','Failure_mob']
        self.historyFile=history_src.historyFile # name of the csv file storing TaskHistory
        Mdata,data=self.reader(self.historyFile,selection_list)
        
        #keep a copy
        Mdata_copy,data_copy=Mdata[:],data[:]
        self.Mdata=Mdata
        self.ip_data=data

        ## RMS calculation
        self.df_rms=self.rms(data,self.task)
        #print(self.df_rms)
        index,tier=self.nearest_match(self.df_rms,Mdata)
        #print('match to ',index,' decision is ',tier)
        self.rms_match=tier

        #fuzzy calculation
        self.fuzzy_op=self.fuzzy(self.task)
        
        if self.fuzzy_op<=50:
            self.fuzzy_op=tuple([self.fuzzy_op,2])
            pass
        else:
            self.fuzzy_op=tuple([self.fuzzy_op,3])
            pass
    
    #get functions
    def get_full_data(self):
        return self.Mdata
    
    def get_ip_data(self):
        return self.ip_data
    
    def get_fuzzy_op(self):
        return self.fuzzy_op

    def get_rms_op(self):
        return tuple([self.df_rms,self.rms_match])

    def get_task(self):
        self.task[1]=int(self.task[1])
        return self.task

    def __init__(self):
        
        x = input("press 1 for input or 2 for interpolation ")
        
        if x=='1':
            #for single
            task=self.runner()
            self.main(task)
        
        elif x=='2':
            # for interpolate run
            tasks=self.runner_interpolate()
            l=len(tasks)
            for i in range(0,l):
                print(tasks[i])
                self.main(tasks[i])

                task=self.get_task()
                full_history=self.get_full_data()
                ip_data=self.get_ip_data()
                rms_output=self.get_rms_op()
                fuzzy_op=self.get_fuzzy_op()

                tier=[fuzzy_op[1]]
                fuzzy_prob=[fuzzy_op[0]]
                fuzzy_prob=round(fuzzy_prob[0],3)
                fuzzy_prob=[fuzzy_prob]
                tier_prob=dummy.probability_calc(fuzzy_op[0])

                record=task+tier+fuzzy_prob+tier_prob

                self.writer(record,history_src.historyFile)
                
                '''
                try:
                    pseudo=input("press ENTER to continue")
                except KeyboardInterrupt:
                    break
                '''
            
            else:
                print("Thank you")
            

obj=Request_analyser()
