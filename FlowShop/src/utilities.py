import math

import numpy as np


# Objective function
def objective(arr, times):
    n_jobs = times.shape[0]
    n_machines = times.shape[1]

    waiting_time = np.zeros((n_jobs, n_machines))

    waiting_time[0, 0] = times[arr[0], 0]
    for time in range(1, n_jobs):
        waiting_time[time, 0] = times[arr[time], 0] + waiting_time[time - 1, 0]

    for machine in range(1, n_machines):
        for time in range(n_jobs):
            final_time = times[arr[time], machine] + np.max([waiting_time[time, machine - 1], waiting_time[time - 1, machine]])
            waiting_time[time, machine] = final_time

    return waiting_time[n_jobs - 1, n_machines - 1]

def read_matrix(filename):

    print("[INFO] Reading file: {}".format(filename))

    with open(filename, "r") as file:
        text = file.read()
    text = text.split("\n")

    [n_jobs, n_machines] = text[0].split()
    n_jobs, n_machines = int(n_jobs), int(n_machines)

    print("[INFO] Matrix's size is {} x {}".format(n_jobs, n_machines))

    times = [np.array(row.split(), dtype=np.int32) for row in text[1:-1]]
    times = np.array(times)
    
    print("[INFO] Matrix is {}".format(times.shape))
    

    print("[INFO] Ended with file: {}".format(filename))
    print("======================")

    return times

def read_report(filename):
    print("[INFO] Reading file: {}".format(filename))

    with open(filename, "r") as file:
        text = file.read()
    text = text.split("\n")

    print(text)

    [n, m, feas_sol] = text[0].split()
    permutation = "".join(text[1:-1])

    print("[INFO] Ended with file: {}".format(filename))
    print("======================")


    return n, m, feas_sol, permutation


