def run_fcfs(processes):
    queue=sorted(processes,key=lambda p:p.arrival_time)
    curr_tick=0
    for process in queue:
        if(curr_tick<process.arrival_time):
            curr_tick=process.arrival_time
        process.start_time=curr_tick
        process.finish_time=curr_tick+process.burst_time
        process.remaining_time=0
        curr_tick=process.finish_time
    
    return processes