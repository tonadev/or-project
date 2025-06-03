import numpy as np

def objective(arr, times):
    cost = 0

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

times = np.array([[5, 1, 9, 3, 10], [2, 6, 7, 8, 4]])
times = times.T

print(times)

arr = np.array([3, 5, 2, 4, 1]) - 1
print(arr)

print(objective(arr, times))