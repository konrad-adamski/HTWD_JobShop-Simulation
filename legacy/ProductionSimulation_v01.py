import math
import random
import simpy
import pandas as pd


def duration_lognormal(duration, vc=0.2):
    """
    Liefert eine Lognormal-verteilte Zufallsdauer basierend auf:
    - duration: gewünschter (aber nicht garantierter) Mittelwert
    - vc: Variationskoeffizient (z. B. 0.2 für 20 %)
    Achtung: Der resultierende Erwartungswert liegt **oberhalb** von duration.
    """
    sigma = vc  # direkt verwenden
    mu = math.log(duration)

    result = random.lognormvariate(mu, sigma)
    return round(result, 2)

df = pd.read_csv("../data/schedule.csv")

simulated_log = []

class Machine(simpy.Resource):
    def __init__(self, env, name):
        super().__init__(env, capacity=1)
        self.name = name


def job_process(env, job_id, job_operations, machines):
    for op in job_operations:
        machine = machines[op["Machine"]]
        start_time = op["Start"]
        planned_duration = op["Duration"]
        sim_duration = duration_lognormal(planned_duration, vc=0.2)  # 👉 simulierte Dauer

        delay = start_time - env.now
        if delay > 0:
            yield env.timeout(delay)             # Warten bis zur geplanten Startzeit

        with machine.request() as req:
            yield req
            sim_start = env.now
            print(f"[{sim_start:.1f}] {job_id} started on {machine.name}")
            yield env.timeout(sim_duration)
            sim_end = env.now
            print(f"[{sim_end:.1f}] {job_id} finished on {machine.name} after {sim_duration} minutes")

        simulated_log.append({ "Job": job_id, "Machine": machine.name, "Start": round(sim_start, 2),
                               "Duration": sim_duration, "End": round(sim_end, 2)
                               })

def run_simulation_from_df(df, until=None):
    env = simpy.Environment()

    # Alle Maschinen extrahieren
    unique_machines = df["Machine"].unique()
    machines = {m: Machine(env, m) for m in unique_machines}

    # Jobs gruppieren
    jobs_grouped = df.groupby("Job")

    # Für jeden Job ein Prozess starten
    for job_id, group in jobs_grouped:
        operations = group.to_dict("records")
        env.process(job_process(env, job_id, operations, machines))

        # Simulation starten – entweder unbegrenzt oder bis 'until'
        if until is not None:
            env.run(until=until)
        else:
            env.run()


if __name__ == "__main__":
    run_simulation_from_df(df)

    # Simulations-DataFrame erzeugen
    df_simulated = pd.DataFrame(simulated_log)

    # Nach Startzeit sortieren
    df_simulated = df_simulated.sort_values(by="Start").reset_index(drop=True)

    #print(df_simulated.head())

