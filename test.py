import numpy as np
from scipy.stats import poisson
from ant_colony import AntColonyOptimizer

class InventoryManagement:
    def __init__(self, num_car_types, critical_levels, pre_critical_levels, holding_costs, order_costs,
                 demand_means, car_weights, truck_capacities, distance_matrix):
        self.num_car_types = num_car_types
        self.critical_levels = critical_levels
        self.pre_critical_levels = pre_critical_levels
        self.holding_costs = holding_costs
        self.order_costs = order_costs
        self.demand_means = demand_means
        self.car_weights = car_weights
        self.truck_capacities = truck_capacities
        self.distance_matrix = distance_matrix

        # Initialize inventory levels and trucks
        self.inventory_levels = np.zeros(num_car_types)
        self.trucks = []
        self.total_cost = 0

    def generate_demand(self):
        """Generate random demand based on Poisson distribution."""
        return [poisson.rvs(mu) for mu in self.demand_means]

    def check_inventory(self):
        """Check inventory levels against critical and pre-critical levels."""
        orders = []

        for i in range(self.num_car_types):
            if self.inventory_levels[i] <= self.critical_levels[i]:
                orders.append(i)
                print(f"Critical level reached for car type {i + 1}. Ordering more.")
            elif self.inventory_levels[i] <= self.pre_critical_levels[i]:
                orders.append(i)
                print(f"Pre-critical level reached for car type {i + 1}. Considering order.")

        return orders

    def place_orders(self, orders):
        """Place orders for the car types that need replenishment."""
        for i in orders:
            order_quantity = max(0, self.critical_levels[i] - self.inventory_levels[i])
            if order_quantity > 0:
                # Update inventory and costs
                self.inventory_levels[i] += order_quantity
                order_cost = self.order_costs[i] + (self.holding_costs[i] * order_quantity)
                self.total_cost += order_cost
                print(f"Placed order for {order_quantity} of car type {i + 1}. Total cost: {order_cost}")

    def allocate_trucks(self, demand):
        """Allocate cars to trucks based on weights and capacities."""
        remaining_truck_capacities = self.truck_capacities[:]
        trucks = [[] for _ in range(len(self.truck_capacities))]

        for i in range(self.num_car_types):
            cars_to_load = demand[i]
            while cars_to_load > 0:
                for j, capacity in enumerate(remaining_truck_capacities):
                    if cars_to_load > 0 and self.car_weights[i] <= capacity:
                        trucks[j].append((i + 1, self.car_weights[i]))
                        remaining_truck_capacities[j] -= self.car_weights[i]
                        cars_to_load -= 1
                        break
                else:
                    print(f"Warning: Not enough capacity to load all cars of type {i + 1}.")
                    break

        self.trucks = trucks
        return trucks

    def optimize_routes(self, trucks):
        """Optimize delivery routes for each truck using an external algorithm."""
        optimized_routes = []
        for truck_id, truck in enumerate(trucks):
            if truck:  # Only optimize routes for trucks with deliveries
                clients = [item[0] for item in truck]  # Extract client IDs
                print("вид клиентов", clients)
                route = self.solve_tsp(self.distance_matrix, clients)
                optimized_routes.append((truck_id, route))
                print(f"Optimized route for truck {truck_id + 1}: {route}")
        return optimized_routes

    def solve_tsp(self, distance_matrix, clients):

        '''optimizer = AntColonyOptimizer(ants=50, evaporation_rate=.1, intensification=2, alpha=1, beta=1,
                                       beta_evaporation_rate=0, choose_best=.1)
        best = optimizer.fit(distance_matrix, 100)
        solution = optimizer.best_path
        # Example placeholder for the algorithm:'''
        print(clients)
        return clients  # Replace with actual optimized path

    def update_inventory(self, demand):
        """Update inventory levels based on generated demand."""
        for i in range(self.num_car_types):
            if demand[i] <= self.inventory_levels[i]:
                self.inventory_levels[i] -= demand[i]
                print(f"Fulfilled demand of {demand[i]} for car type {i + 1}.")
            else:
                unmet_demand = demand[i] - self.inventory_levels[i]
                print(f"Unmet demand of {unmet_demand} for car type {i + 1}.")
                self.inventory_levels[i] = 0

    def simulate(self, time_period):
        """Simulate the inventory management over a specified time period."""
        for t in range(time_period):
            print(f"\nTime period {t + 1}:")
            demand = self.generate_demand()
            print(f"Generated demand: {demand}")

            # Update inventory based on demand
            self.update_inventory(demand)

            # Check inventory levels and place orders if necessary
            orders = self.check_inventory()
            if orders:
                self.place_orders(orders)

            # Allocate cars to trucks
            trucks = self.allocate_trucks(demand)
            print(f"Truck allocations: {trucks}")

            # Optimize delivery routes for each truck
            optimized_routes = self.optimize_routes(trucks)

        print(f"\nTotal costs incurred: {self.total_cost}")



num_car_types = 4
critical_levels = [10, 15, 20, 5]
pre_critical_levels = [15, 20, 25, 10]
holding_costs = [1.0, 1.5, 2.0, 0.5]
order_costs = [50, 75, 100, 25]
demand_means = [12, 18, 22, 8]
car_weights = [2, 3, 4, 1]
truck_capacities = [15, 20, 25]
dig = 15
matrix = [[0 for x in range(dig)] for y in range(dig)]

inventory_manager = InventoryManagement(num_car_types, critical_levels, pre_critical_levels,
                                        holding_costs, order_costs, demand_means,
                                        car_weights, truck_capacities, matrix)

inventory_manager.simulate(12)