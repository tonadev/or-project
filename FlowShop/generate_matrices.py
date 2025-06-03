from os.path import join

import numpy as np

MATRICES_FILENAME = "matrices.txt"
MATRICES_DIR = "./matrices"

with open(MATRICES_FILENAME, "r") as file:
    text = file.read()
text = text.split("\n")

i = 0
while i < len(text):
    i += 2
    instance_name = text[i].split()[1]
    i += 4

    print("[INFO] Starting reading matrix {}".format(instance_name))

    [n_jobs, n_machines] = text[i].split() # read n_jobs and n_machines

    n_jobs = int(n_jobs)
    n_machines = int(n_machines)

    i += 1

    matrix = list()
    for j in range(i, i + n_jobs):
        line = text[j].split() # read matrix line
        row = list()
        
        for k in range(1, n_machines * 2, 2):
            row.append(int(line[k]))
        
        matrix.append(row)

    matrix = np.array(matrix)

    filepath = join(MATRICES_DIR, instance_name + ".txt")
                    

    np.savetxt(filepath, matrix, fmt="%d")
    
    with open(filepath, "r") as file:
        mat = file.read()

    with open(filepath, "w") as file:
        file.write("{} {}\n".format(n_jobs, n_machines))
        file.write(mat)

    print("[INFO] Ended reading matrix. No. jobs: {}, No. machines: {}".format(matrix.shape[0], matrix.shape[1]))

    i += n_jobs