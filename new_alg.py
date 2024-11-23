weights = [750, 650, 800, 700]

clients = {
    1: {0: 2, 1: 2, 2: 1, 3: 1},
    2: {0: 1, 1: 2, 2: 2, 3: 1},
    3: {0: 3, 1: 1, 2: 1, 3: 2},
    4: {0: 2, 1: 1, 2: 2, 3: 1},
    5: {0: 2, 1: 2, 2: 1, 3: 2},
    6: {0: 1, 1: 1, 2: 2, 3: 2},
    7: {0: 1, 1: 1, 2: 1, 3: 1},
    8: {0: 1, 1: 1, 2: 1, 3: 1},
    9: {0: 1, 1: 1, 2: 1, 3: 1},
    10: {0: 1, 1: 1, 2: 2, 3: 1},
}

truck_capacity = 5000

def greedy_allocation(clients, truck_capacity, weights):
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

    return truck_clients


truck_clients = greedy_allocation(clients, truck_capacity, weights)
truck_dict = {truck_id + 1: sorted(set(clients_assigned)) for truck_id, clients_assigned in enumerate(truck_clients)}
print(truck_dict)