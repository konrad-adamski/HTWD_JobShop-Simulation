
import random


JOB_COLORS = [
    "#1E90FF",  # kräftiges Blau (DodgerBlue)
    "#00CED1",  # Türkisblau (DarkTurquoise)
    "#228B22",  # sattes Dunkelgrün (ForestGreen)
    "#ADFF2F",  # helles Gelbgrün (GreenYellow)
    "#FFD700",  # reines Gelb (Gold)
    "#B8860B",  # dunkleres Goldbraun (DarkGoldenrod)
    "#8B4513",  # sattes Braun (SaddleBrown)
    "#D2691E",  # warmes Rostbraun (Chocolate)
    "#800080",  # klassisches Violett (Purple)
    "#BA55D3",  # helles, freundliches Violett (MediumOrchid)
]


class Job:
    def __init__(self, job_id):
        self.job_id = job_id
        self.color = self._pick_color()

    def _pick_color(self):
        job_id_str = str(self.job_id)
        last_two_chars = job_id_str[-2:].strip()
        if last_two_chars.isdigit():
            last_two_digits = int(last_two_chars)
        else:
            last_two_digits = 0
        return JOB_COLORS[last_two_digits % len(JOB_COLORS)]




class Operation:
    def __init__(self, job: Job, machine_name, start_time, duration):
        self.job = job  # <-- Direkte Referenz auf den Job
        self.machine_name = machine_name
        self.start_time = start_time
        self.duration = duration
