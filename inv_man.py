import numpy as np
from scipy.stats import poisson
from ant_colony import start_algorithm
import random

class InventoryManagement:
    def __init__(self, num_car_types, critical_levels, pre_critical_levels, holding_costs, order_costs, demand_means):
        # Количество типов автомобилей
        self.num_car_types = num_car_types
        # Критический уровень запасов
        self.critical_levels = critical_levels
        # Предкритический уровень запапсов
        self.pre_critical_levels = pre_critical_levels
        # Расходы на хранение
        self.holding_costs = holding_costs
        # Цена заказа
        self.order_costs = order_costs
        # Спрос
        self.demand_means = demand_means
        
        # Initialize inventory levels
        self.inventory_levels = np.zeros(num_car_types)
        self.total_cost = 0
        

    def generate_demand(self):
        """ Генерация случайного спроса на основе распределения Пуассона. """
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


    def update_inventory(self, demand):
        """ Обновление уровня запасов на основе сформированного спроса """
        for i in range(self.num_car_types):
            if demand[i] <= self.inventory_levels[i]:
                self.inventory_levels[i] -= demand[i]
                print(f"Fulfilled demand of {demand[i]} for car type {i + 1}.")
            else:
                unmet_demand = demand[i] - self.inventory_levels[i]
                print(f"Unmet demand of {unmet_demand} for car type {i + 1}.")
                self.inventory_levels[i] = 0


    def generate_clients(self, dig):
        # Создаем пустую матрицу размером 50 на 50
        matrix = [[0 for x in range(dig)] for y in range(dig)]

        # Заполняем матрицу случайными числами
        for i in range(dig):
            for j in range(dig):
                if i == j:
                    matrix[i][j] = 0
                else:
                    value = random.randint(100, 1000)
                    matrix[i][j] = value
                    matrix[j][i] = value

        return matrix
    


    def call_routing(self):
        matrix = self.generate_clients(dig = 10)


        best, solution = start_algorithm(matrix)

        
        print(f"Длина пути: {best}")


    def simulate(self, time_period):
        """ Моделировать управление запасами за указанный период времени """
        for t in range(time_period):
            print(f"\nTime period {t + 1}:")
            # Генерация спроса
            demand = self.generate_demand()
            print(f"Generated demand: {demand}")
            
            # Обновление склада в соответствии со спросом
            self.update_inventory(demand)

            # Запуск маршрутизации
            self.call_routing()
            
            # Проверка уровня запасов
            orders = self.check_inventory()

            if orders:
                # Восполнение запасов
                self.place_orders(orders)

        print(f"\nTotal costs incurred: {self.total_cost}")





### Пример параметров
# Количество типов автомобилей
num_car_types = 4
# Критический уровень запасов
critical_levels = [10, 15, 20, 5]
# Предкритический уровень запапсов
pre_critical_levels = [15, 20, 25, 10]
# Расходы на хранение
holding_costs = [1.0, 1.5, 2.0, 0.5]
# Цена заказа
order_costs = [50, 75, 100, 25]
# Спрос
demand_means = [12, 18, 22, 8]

# Инициализация стартовых параметров управления запасами
inventory_manager = InventoryManagement(num_car_types, 
                                        critical_levels, 
                                        pre_critical_levels,
                                        holding_costs, 
                                        order_costs, 
                                        demand_means)

# Вызов симуляции управления запасов на заданное количество месяцев
inventory_manager.simulate(12)