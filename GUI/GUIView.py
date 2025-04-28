import tkinter as tk
import pandas as pd
from Controller import Controller
from ProductionDaySimulation import ProductionDaySimulation


from GanttCanvas import GanttCanvas  # NEU!

class GUIView:
    def __init__(self, root):
        self.root = root

        # --- Haupt-Frame ---
        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        # --- Gantt-Canvas (links) ---
        self.gantt_canvas = GanttCanvas(self.main_frame)
        self.gantt_canvas.pack(side="left")

        # --- Legenden-Canvas (rechts) ---
        self.legend_canvas = tk.Canvas(self.main_frame, width=128, height=576, bg="white")
        self.legend_canvas.pack(side="left")

    def setup_machines(self, machines):
        self.gantt_canvas.setup_machines(machines)

    def add_operation(self, operation, color="blue"):
        self.gantt_canvas.add_operation(operation, color)

    def finish_operation(self, job_id, machine_name, time_stamp, color, break_bool=False):
        self.gantt_canvas.finish_operation(job_id, machine_name, time_stamp, color, break_bool)

    def break_operation(self, job_id, machine_name):
        self.gantt_canvas.break_operation(job_id, machine_name)

    def draw_legend(self, jobs):
        spacing = 25
        start_x = 10
        start_y = 50

        self.legend_canvas.create_text(start_x, start_y - 30, text="Legende:", anchor="w", font=("Arial", 12, "bold"))

        for idx, (job_id, job) in enumerate(sorted(jobs.items())):
            y = start_y + idx * spacing

            self.legend_canvas.create_rectangle(
                start_x, y,
                start_x + 20, y + 20,
                fill=job.color,
                outline=job.color
            )

            self.legend_canvas.create_text(
                start_x + 30, y + 10,
                text=f"{job_id}",
                anchor="w"
            )



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Live Gantt Chart - Production Simulation")

    # Lade Tagesplan
    df_schedule_plan = pd.read_csv("data/schedule.csv")

    # Setze alles zusammen
    gui_view = GUIView(root)
    controller = Controller(gui_view)
    simulation = ProductionDaySimulation(df_schedule_plan, vc=0.25)
    simulation.set_controller(controller)

    gui_view.setup_machines(simulation.machines.keys())
    gui_view.draw_legend(controller.jobs)

    # Starte Simulation in neuem Thread (damit GUI nicht blockiert)
    import threading

    def run_simulation():
        simulation.run()

    sim_thread = threading.Thread(target=run_simulation)
    sim_thread.start()

    root.mainloop()
