def get_waittime(processes):
    return [p.finish_time-p.arrival_time-p.burst_time for p in processes]

def mean_waittime(processes):
    wait_times=get_waittime(processes)
    return sum(wait_times)/len(wait_times)

def p90_waittime(processes):
    wait_times=sorted(get_waittime(processes))
    idx=int(0.9*len(wait_times))
    return wait_times[idx]

def jfidx(processes):
    wait_times=get_waittime(processes)
    num=sum(wait_times)**2
    den=len(wait_times)*(w**2 for w in wait_times)
    if den==0:
        return 1.0
    return num/den

def evaluate(processes):
    return{
        "mwt":mean_waittime(processes),
        "p90wt":p90_waittime(processes),
        "jfi":jfidx(processes)
    }