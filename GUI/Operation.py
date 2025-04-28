from Job import Job


class Operation:
    def __init__(self, job: Job, machine_name, start_time, duration):
        self.job = job  # <-- Direkte Referenz auf den Job
        self.machine_name = machine_name
        self.start_time = start_time
        self.duration = duration
