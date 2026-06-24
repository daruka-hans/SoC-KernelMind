import random

def run_rs(processes,quantum=3):
    remaining=list(processes)
    curr_tick=0
    completed=[]

    while remaining:
        available=[p for p in remaining if p.arrival_time<=curr_tick]
        if not available:
            curr_tick=min(p.arrival_time for p in remaining)
            continue

        chosen=random.choice(available)
        if chosen.start_time is None:
            chosen.start_time=curr_tick
        
        if chosen.remainng_time<=quantum:
            curr_tick+=chosen.remaining_time
            chosen.remaining_time=0
            chosen.finish_time=curr_tick
            completed.append(chosen)
            remaining.remove(chosen)
        else:
            chosen.remaining_time-=quantum
            curr_tick+=quantum
        
    return completed
