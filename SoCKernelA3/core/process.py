class Process:
    def __init__(self,pid,burst_time,arrival_time):
        self.pid=pid
        self.burst_time=burst_time
        self.arrival_time=arrival_time
        self.remaining_time=burst_time
        self.start_time=None
        self.finish_time=None