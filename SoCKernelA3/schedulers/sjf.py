def run_sjf(processes):
    remaining=list(processes)
    curr_tick=0
    completed=[]

    while remaining:
        available=[p for p in remaining if p.arrival_time<=curr_tick]
        if not available:
            curr_tick=min(p.arrival_time for p in remaining)
            continue
        
        chosen=min(available,key=lambda p:p.burst_time)
        chosen.start_time=curr_tick
        chosen.finish_time=curr_tick+chosen.burst_time
        chosen.remaining_time=0
        curr_tick=chosen.finish_time

        remaining.remove(chosen)
        completed.append(chosen)
    
    return completed