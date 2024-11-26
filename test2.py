import random
from ant_colony import start_algorithm

n = 11
matrix = [[0] * n for _ in range(n)]

for i in range(n):
    for j in range(i + 1, n):
        value = random.randint(50, 5000)
        matrix[i][j] = value
        matrix[j][i] = value

subsets = {1: [1], 2: [2, 3], 3: [3, 4], 4: [4, 5], 5: [5, 6], 6: [6, 7], 7: [7, 8, 9], 8: [9, 10]}


def extract_mini_matrix(matrix, indices):
    full_indices = [0] + indices
    return [[matrix[i][j] for j in full_indices] for i in full_indices]


mini_matrices = {}
for key, indices in subsets.items():
    mini_matrices[key] = extract_mini_matrix(matrix, indices)

dist_list = []
for i in range(1, len(mini_matrices)+1):
    ds = start_algorithm(mini_matrices[i])
    dist_list.append(ds)


def calc_cost(dig):
    return round(dig / 100 * 30 * 45, 1)


cost_list = list(map(calc_cost, dist_list))
print(sum(cost_list))


