import history_src 
from history_src import History

import Request_analyser_src
from Request_analyser_src import Request_analyser

import Service_broker
import dummy

obj=Request_analyser()


#check gets()
task=obj.get_task()
full_history=obj.get_full_data()
ip_data=obj.get_ip_data()
rms_output=obj.get_rms_op()
fuzzy_op=obj.get_fuzzy_op()

print(task)
#print(full_history)
#print(ip_data)
#print(rms_output)
print(fuzzy_op)

sla_score=Service_broker.sla_comparator(task)
print(sla_score)


tier=[fuzzy_op[1]]
fuzzy_prob=[fuzzy_op[0]]
tier_prob=dummy.probability_calc(fuzzy_op[0])


record=task+tier+fuzzy_prob+tier_prob

obj.writer(record,history_src.historyFile)
