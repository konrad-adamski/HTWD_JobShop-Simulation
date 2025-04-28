import tkinter as tk


class GanttCanvas(tk.Canvas):
    def __init__(self, parent, total_minutes=1440, width=1024, height=576, **kwargs):
        super().__init__(parent, width=width, height=height, bg="white", **kwargs)
        self.total_minutes = total_minutes
        self.width = width
        self.height = height

        self.x_offset = 80  # Verschiebung nach rechts für Maschinen-Namen
        self.right_padding = 40  # Rechts Platz lassen für "24h" Schrift
        self.operation_half_height = 14  # Höhe der Operationen nach oben und unten

        self.usable_width = self.width - self.x_offset - self.right_padding  # NEU: feste usable_width

        self.machine_positions = {}
        self.operations = {}

        # self.draw_time_axis()

    def draw_time_axis(self):
        """Zeichnet die Zeitachse (oben) von 0 bis total_minutes."""
        num_ticks = 12  # z.B. alle 2 Stunden
        interval = self.total_minutes // num_ticks
        pixels_per_minute = self.usable_width / self.total_minutes

        for i in range(num_ticks + 1):
            minutes = i * interval
            x = self.x_offset + minutes * pixels_per_minute

            # Kurzer Strich oben
            self.create_line(x, 0, x, 10, fill="black")

            # Zeitbeschriftung
            hours = minutes // 60
            self.create_text(x + 5, 12, text=f"{hours}h", anchor="nw", font=("Arial", 8))

            # Gestrichelte Linie nach unten
            self.create_line(x, 20, x, self.height, fill="gray", dash=(2, 4))

    def setup_machines(self, machines):
        initial_offset = 60  # Abstand der ersten Maschine
        spacing = 50  # Abstand zwischen den Maschinen
        num_machines = len(machines)
        new_height = max(initial_offset + (num_machines - 1) * spacing + 20, int(self.height))

        self.config(height=new_height)
        self.height = new_height
        self.draw_time_axis()

        for idx, machine in enumerate(sorted(machines)):
            y = initial_offset + idx * spacing
            self.machine_positions[machine] = y
            self.create_text(20, y, text=machine, anchor="w", font=("Helvetica", 12, "bold"))


    def add_operation(self, operation, color="blue"):
        y = self.machine_positions[operation.machine_name]
        pixels_per_minute = self.usable_width / self.total_minutes
        x_start = self.x_offset + operation.start_time * pixels_per_minute

        rect = self.create_rectangle(
            x_start, y - self.operation_half_height,
            x_start + 5, y + self.operation_half_height,
            fill=color,
            outline=color
        )
        self.operations[(operation.job.job_id, operation.machine_name)] = (operation, rect)

    def finish_operation(self, job_id, machine_name, time_stamp, color, timeout_bool=False):
        key = (job_id, machine_name)
        if key in self.operations:
            operation, rect = self.operations[key]
            pixels_per_minute = self.usable_width / self.total_minutes
            x_start = self.x_offset + operation.start_time * pixels_per_minute
            x_end = self.x_offset + time_stamp * pixels_per_minute
            y = self.machine_positions[machine_name]

            self.coords(rect, x_start, y - self.operation_half_height, x_end, y + self.operation_half_height)
            self.itemconfig(rect, fill=color)

            if timeout_bool:
                for offset in range(int(x_start), int(x_end+2), 6):
                    self.create_line(
                        offset + 6 , y - self.operation_half_height,
                        offset - 3, y + self.operation_half_height,
                        fill="red", width=1
                    )

    def break_operation(self, job_id, machine_name):
        key = (job_id, machine_name)
        if key in self.operations:
            _, rect = self.operations[key]
            self.itemconfig(rect, fill="red")
