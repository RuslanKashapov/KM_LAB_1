import random
from ant_colony import start_algorithm


def calc_cost(dig):
    return round(dig / 100 * 30 * 45, 1)


def extract_mini_matrix(matrix, indices):
    full_indices = [0] + indices
    return [[matrix[i][j] for j in full_indices] for i in full_indices]


def cost_function(truck_dict, matrix):
    mini_matrices = {}
    for key, indices in truck_dict.items():
        mini_matrices[key] = extract_mini_matrix(matrix, indices)

    dist_list = []
    for i in range(1, len(mini_matrices)+1):
        ds = start_algorithm(mini_matrices[i])
        dist_list.append(ds)

    cost_list = list(map(calc_cost, dist_list))
    return sum(cost_list)


def greedy_allocation(clients):
    weights = [750, 650, 800, 700]
    truck_capacity = 5000
    truck_clients = []
    truck_capacities = []

    for client_id, demand in clients.items():
        for cargo_id, amount in demand.items():
            total_weight = amount * weights[cargo_id]

            while total_weight > 0:
                assigned = False
                for i in range(len(truck_capacities)):
                    if truck_capacities[i] >= total_weight:
                        truck_clients[i].append(client_id)
                        truck_capacities[i] -= total_weight
                        total_weight = 0
                        assigned = True
                        break
                    elif truck_capacities[i] > 0:
                        truck_clients[i].append(client_id)
                        total_weight -= truck_capacities[i]
                        truck_capacities[i] = 0
                        assigned = True

                if not assigned:
                    if total_weight > truck_capacity:
                        truck_clients.append([client_id])
                        truck_capacities.append(0)
                        total_weight -= truck_capacity
                    else:
                        truck_clients.append([client_id])
                        truck_capacities.append(truck_capacity - total_weight)
                        total_weight = 0
    truck_dict = {truck_id + 1: sorted(set(clients_assigned)) for truck_id, clients_assigned in enumerate(truck_clients)}
    return truck_dict


def cargo_distribution(clients, matrix):
    truck_dict =  greedy_allocation(clients)
    cost = cost_function(truck_dict, matrix)
    return cost
