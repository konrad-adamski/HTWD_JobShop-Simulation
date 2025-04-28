import tkinter as tk
import pandas as pd
from Controller import Controller
from ProductionDaySimulation import ProductionDaySimulation


class GUIView:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=1024, height=648, bg="white")
        self.canvas.pack()

        self.machine_positions = {}
        self.operations = {}

    def setup_machines(self, machines):
        spacing = 60
        for idx, machine in enumerate(sorted(machines)):
            y = (idx + 1) * spacing
            self.machine_positions[machine] = y
            self.canvas.create_text(20, y, text=machine, anchor="w")

    def add_operation(self, operation, color="blue"):
        y = self.machine_positions[operation.machine_name]
        x_start = operation.start_time / 2  # Skaliere Zeit

        rect = self.canvas.create_rectangle(
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

            self.canvas.coords(rect, x_start, y - 10, x_end, y + 10)
            self.canvas.itemconfig(rect, fill=color)

            if break_bool:
                # Gestreifte Linien draufmalen
                for offset in range(int(x_start), int(x_end), 6):  # alle 6 Pixel
                    self.canvas.create_line(
                        offset, y - 10,
                                offset - 5, y + 10,
                        fill="lightblue", width=1
                    )

    def break_operation(self, job_id, machine_name):
        key = (job_id, machine_name)
        if key in self.operations:
            _, rect = self.operations[key]
            self.canvas.itemconfig(rect, fill="red")





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

    # Starte Simulation in neuem Thread (damit GUI nicht blockiert)
    import threading

    def run_simulation():
        simulation.run()

    sim_thread = threading.Thread(target=run_simulation)
    sim_thread.start()

    root.mainloop()