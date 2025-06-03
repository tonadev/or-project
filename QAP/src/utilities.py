import math

import numpy as np


# Objective function
def objective(x, distances, flows):
    cost = 0
    for i in range(x.size):
        for j in range(x.size):
            cost += distances[i, j] * flows[x[i], x[j]]
    return cost

def extract_matrix(data, size, begin, omit):
    i = omit
    while data[begin + i] == "":
        i += 1
    step = begin + i

    mat = list()
    for i in range(size):
        start = (i * math.ceil(size / 20)) + step
        end = start + math.ceil(size / 20)

        row = [np.array(row.split(), dtype=np.int32) for row in data[start:end]]
        mat.append(np.concatenate(row))
    mat = np.array(mat)

    return mat, end

def read_matrix(filename):

    print("[INFO] Reading file: {}".format(filename))

    with open(filename, "r") as file:
        text = file.read()
    text = text.split("\n")

    n = int(text[0])

    print("[INFO] Matrix's size is {}".format(n))

    [distances, end] = extract_matrix(text, n, 0, 1)

    print("[INFO] First matrix is {}".format(distances.shape))
    
    [flows, _] = extract_matrix(text, n, end, 0)

    print("[INFO] Second matrix is {}".format(flows.shape))
    

    print("[INFO] Ended with file: {}".format(filename))
    print("======================")

    return distances, flows

def read_report(filename):
    print("[INFO] Reading file: {}".format(filename))

    with open(filename, "r") as file:
        text = file.read()
    text = text.split("\n")

    print(text)

    [n, feas_sol] = text[0].split()
    permutation = "".join(text[1:-1])

    print("[INFO] Ended with file: {}".format(filename))
    print("======================")


    return n, feas_sol, permutation


