import tkinter as tk
import pandas as pd
from Controller import Controller
from ProductionDaySimulation import ProductionDaySimulation


class GUIView:
    def __init__(self, root):
        self.root = root

        # --- Haupt-Frame ---
        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        # --- Gantt-Canvas (links) ---
        self.gantt_canvas = tk.Canvas(self.main_frame, width=740, height=648, bg="white")
        self.gantt_canvas.pack(side="left")

        # --- Legenden-Canvas (rechts) ---
        self.legend_canvas = tk.Canvas(self.main_frame, width=128, height=648, bg="white")
        self.legend_canvas.pack(side="left")

        self.machine_positions = {}
        self.operations = {}

    def setup_machines(self, machines):
        spacing = 60
        for idx, machine in enumerate(sorted(machines)):
            y = (idx + 1) * spacing
            self.machine_positions[machine] = y
            self.gantt_canvas.create_text(20, y, text=machine, anchor="w")

    def add_operation(self, operation, color="blue"):
        y = self.machine_positions[operation.machine_name]
        x_start = operation.start_time / 2  # Skaliere Zeit

        rect = self.gantt_canvas.create_rectangle(
            x_start, y - 10,
            x_start + 5, y + 10,
            fill=color,
            outline=color
        )
        self.operations[(operation.job.job_id, operation.machine_name)] = (operation, rect)

    def finish_operation(self, job_id, machine_name, time_stamp, color, break_bool=False):
        key = (job_id, machine_name)
        if key in self.operations:
            operation, rect = self.operations[key]
            x_start = operation.start_time / 2
            x_end = time_stamp / 2
            y = self.machine_positions[machine_name]

            self.gantt_canvas.coords(rect, x_start, y - 10, x_end, y + 10)
            self.gantt_canvas.itemconfig(rect, fill=color)

            if break_bool:
                for offset in range(int(x_start), int(x_end), 6):  # alle 6 Pixel
                    self.gantt_canvas.create_line(
                        offset, y - 10,
                        offset - 5, y + 10,
                        fill="lightblue", width=1
                    )

    def break_operation(self, job_id, machine_name):
        key = (job_id, machine_name)
        if key in self.operations:
            _, rect = self.operations[key]
            self.gantt_canvas.itemconfig(rect, fill="red")

    def draw_legend(self, jobs):
        spacing = 25
        start_x = 10
        start_y = 50

        # "Legende"-Überschrift
        self.legend_canvas.create_text(start_x, start_y - 30, text="Legende:", anchor="w", font=("Arial", 12, "bold"))

        for idx, (job_id, job) in enumerate(sorted(jobs.items())):
            y = start_y + idx * spacing

            # Farbfeld
            self.legend_canvas.create_rectangle(
                start_x, y,
                start_x + 20, y + 20,
                fill=job.color,
                outline=job.color
            )

            # Text daneben
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
