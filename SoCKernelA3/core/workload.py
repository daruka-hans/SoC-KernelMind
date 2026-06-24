import random
from core.process import Process

def generate_workload(n=10,max_burst=20,max_arrival=10):
    processes=[]
    for pid in range(n):
        arrival=random.randint(0,max_arrival)
        burst=random.randint(1,max_burst)
        processes.append(Process(pid,burst,arrival))
    return sorted(processes, key=lambda p:p.arrival_time)