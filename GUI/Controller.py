from GUI.Operation import Operation
from Job import Job
from Machine import Machine

class Controller:
    def __init__(self, gui_view=None):
        self.gui_view = gui_view
        self.simulation = None
        self.machines = {}
        self.jobs = {}  # <-- Ergänzt: Dictionary für alle Jobs
        self.job_color_idx = 0
        self.operations = {}  # <-- Ergänzt: Dictionary für aktive Operationen (optional, für Zugriff später)

    def job_started_on_machine(self, time_stamp, job_id, machine):
        job = self.jobs[job_id]
        operation = Operation(job, machine.name, time_stamp, None)

        # Merke dir die Operation unter (job_id, machine_name)
        self.operations[(job_id, machine.name)] = operation

        # Hier: Color holen aus dem Job
        color = job.color

        if self.gui_view:
            self.gui_view.add_operation(operation, color)

    def job_finished_on_machine(self, time_stamp, job_id, machine, sim_duration):
        key = (job_id, machine.name)
        if key in self.operations: # wozu???
            operation = self.operations[key]
            operation.duration = sim_duration
        else:
            print(f"Warning: No operation found for {key}!")

        # Hier: Color holen aus dem Job
        color = self.jobs[job_id].color

        if self.gui_view:
            self.gui_view.finish_operation(job_id, machine.name, time_stamp, color)


    def job_time_out(self, job_id, machine_name):
        # Hier: Color holen aus dem Job
        color = self.jobs[job_id].color

        if self.gui_view:
            self.gui_view.finish_operation(job_id, machine_name, 1440, color, True)

    def add_machines(self, *machines: Machine):
        for machine in machines:
            self.machines[machine.name] = machine


    def update_jobs(self, *jobs_ids: str):
        job_id_list = list(jobs_ids)  # NICHT als Set!

        self.job_color_idx = 0

        # 1. Neue Jobs hinzufügen
        for job_id in job_id_list:
            if job_id not in self.jobs:
                self.jobs[job_id] = Job(job_id, self.job_color_idx)
                self.job_color_idx += 1

        # 2. Alte Jobs entfernen
        old_job_ids = set(self.jobs.keys())
        new_job_ids = set(job_id_list)

        jobs_to_remove = old_job_ids - new_job_ids

        for job_id in jobs_to_remove:
            del self.jobs[job_id]

    def handle_undone(self, df_undone):
        for _, row in df_undone[df_undone["Start"].notna()].iterrows():
            job_id = row["Job"]
            machine = row["Machine"]
            self.job_time_out(job_id, machine)


