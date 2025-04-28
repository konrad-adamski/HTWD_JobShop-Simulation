from GUI.GUI_Classes import Job, Operation
from Machine import Machine

class Controller:
    def __init__(self, gui_view=None):
        self.gui_view = gui_view
        self.simulation = None
        self.machines = {}
        self.jobs = {}  # <-- Ergänzt: Dictionary für alle Jobs
        self.operations = {}  # <-- Ergänzt: Dictionary für aktive Operationen (optional, für Zugriff später)

    def job_started_on_machine(self, time_stamp, job_id, machine):
        if job_id not in self.jobs:
            self.jobs[job_id] = Job(job_id)

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
        if key in self.operations:
            operation = self.operations[key]
            operation.duration = sim_duration
        else:
            print(f"Warning: No operation found for {key}!")

        # Hier: Color holen aus dem Job
        color = self.jobs[job_id].color

        if self.gui_view:
            self.gui_view.finish_operation(job_id, machine.name, time_stamp, color)


    def job_break(self, job_id, machine, time_stamp):
        # Hier: Color holen aus dem Job
        color = self.jobs[job_id].color

        if self.gui_view:
            self.gui_view.finish_operation(job_id, machine.name, time_stamp, color, True)
            self.gui_view.break_operation(job_id, machine.name)

    def add_machines(self, *machines: Machine):
        for machine in machines:
            self.machines[machine.name] = machine


