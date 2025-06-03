import numpy as np

def castling(arr):
  size = arr.size

  r1, r2 = np.random.randint(low=0, high=size, size=2)

  swapped = arr.copy()
  swapped[[r1, r2]] = swapped[[r2, r1]]

  yield swapped

def shifting(arr):
  size = arr.size

  r1, r2 = np.random.randint(low=0, high=size, size=2)
  left = np.min([r1, r2])
  right = np.max([r1, r2])

  swapped = arr.copy()
  temp = swapped[left]
  swapped[left:right] = swapped[left + 1:right + 1]
  swapped[right] = temp

  yield swapped

def right_swap(arr):
  size = arr.size
  for i in range(size - 1):
    swapped = arr.copy()
    swapped[[i, i + 1]] = swapped[[i + 1, i]]

    yield swapped

def two_swap(arr):
    size = arr.size
    for i in range(size):
      for j in range(i + 1, size):
        swapped = arr.copy()
        swapped[[i, j]] = swapped[[j, i]]

        yield swapped


def three_swap(arr):
  size = arr.size
  for i in range(size):
    for j in range(i + 1, size):
      for k in range(j + 1, size):
        swapped = arr.copy()
        swapped[[i, j, k]] = swapped[[j, k, i]]
        yield swapped

        swapped = arr.copy()
        swapped[[i, j, k]] = swapped[[k, i, j]]
        yield swapped

def two_opt(arr):
  size = arr.size

  r1, r2 = np.random.randint(low=0, high=size, size=2)
  left = np.min([r1, r2])
  right = np.max([r1, r2])

  swapped = arr.copy()
  swapped[left:right + 1] = swapped[left:right + 1][::-1]

  yield swapped