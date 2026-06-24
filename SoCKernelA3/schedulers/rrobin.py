from collections import deque

def run_rr(processes,quantum=3):
    arrivals=sorted(processes,key=lambda p:p.arrival_time)
    ready_queue=deque()
    completed=[]
    curr_tick=0
    arr_idx=0
    ticks_used=0

    while arr_idx<len(arrivals) and arrivals[arr_idx].arrival_time<=curr_tick:       #load processes that arrive at tick 0
        ready_queue.append(arrivals[arr_idx])
        arr_idx+=1

    while ready_queue or arr_idx<len(arrivals):
        if not ready_queue:
            curr_tick=arrivals[arr_idx].arrival_time
            while arr_idx<len(arrivals) and arrivals[arr_idx].arrival_time<=curr_tick:
                ready_queue.append(arrivals[arr_idx])
                arr_idx+=1
            ticks_used=0
            continue

        process=ready_queue[0]
        if process.start_time is None:
            process.start_time=curr_tick

        process.remaining_time-=1     #run 1 tick
        curr_tick+=1
        ticks_used+=1

        while arr_idx<len(arrivals) and arrivals[arr_idx].arrival_time<=curr_tick:    #add processes that came after this tick to the queue
            ready_queue.append(arrivals[arr_idx])
            arr_idx+=1

        if process.remaining_time==0:
            process.finish_time=curr_tick
            ready_queue.popleft()
            completed.append(process)
            ticks_used=0

        elif ticks_used==quantum:
            ready_queue.popleft(process)
            ready_queue.append(process)
            ticks_used=0

    return completed