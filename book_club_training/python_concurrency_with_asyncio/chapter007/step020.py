import numpy as np
import time


data_points = 400_000_000
rows = 50
columns = data_points // rows

matrix = np.arange(data_points).reshape(rows, columns)

start = time.perf_counter()
res = np.mean(matrix, axis=1)
end = time.perf_counter()
print(end - start)
print(len(res))
