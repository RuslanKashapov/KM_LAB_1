import numpy as np
from scipy.stats import poisson
from ant_colony import start_algorithm
from cargo_distribution import cargo_distribution
import random

class InventoryManagement:
    def __init__(self, num_car_types, critical_levels, pre_critical_levels, holding_costs, order_costs, demand_means, dig):
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

        # Генерация матрицы клиентов
        self.dig = dig
        self.clients_matrix = self.generate_clients(self.dig)
        
        # Initialize inventory levels
        # self.inventory_levels = np.zeros(num_car_types)
        self.inventory_levels = self.pre_critical_levels[:]
        self.total_cost = 0
        

    def generate_demand(self):
        """ Генерация случайного спроса на основе распределения Пуассона. """
        demands = [poisson.rvs(mu) for mu in self.demand_means]
        while sum(demands) < 1:
            demands = [poisson.rvs(mu) for mu in self.demand_means]
        return demands
    

    def check_inventory(self):
        """ Проверка уровни запасов на соответствие критическим и предкритическим уровням """
        orders = []
        
        for i in range(self.num_car_types):
            if self.inventory_levels[i] <= self.critical_levels[i]:
                orders.append(i)
                print(f"Достигнут критический уровень для типа автомобиля {i + 1}. Заказываю еще.")
            elif self.inventory_levels[i] <= self.pre_critical_levels[i]:
                orders.append(i)
                print(f"Достигнут предкритический уровень для типа автомобиля {i + 1}. Заказываю еще.")
                
        return orders


    def place_orders(self, orders):
        """ Размещение заказов на те типы автомобилей, которые требуют пополнения. """
        for i in orders:
            # order_quantity = max(0, self.critical_levels[i] - self.inventory_levels[i])

            # Заказ происходит на значение (разницы между текущим уровням запаса и предкретического уровня) умноженное на 2
            order_quantity = max(0, self.pre_critical_levels[i] - self.inventory_levels[i]) * 2
            if order_quantity > 0:
                # Update inventory and costs
                self.inventory_levels[i] += order_quantity
                order_cost = self.order_costs[i] + (self.holding_costs[i] * order_quantity)
                self.total_cost += order_cost
                print(f"Размещен заказ на {order_quantity} для типа автомобиля {i + 1}. Стомость: {order_cost}")


    def update_inventory(self, demand):
        """ Обновление уровня запасов на основе сформированного спроса """
        for i in range(self.num_car_types):
            if demand[i] <= self.inventory_levels[i]:
                self.inventory_levels[i] -= demand[i]
                print(f"Удовлетворенный спрос на {demand[i]} для типа машины {i + 1}.")
            else:
                unmet_demand = demand[i] - self.inventory_levels[i]
                print(f"Неудовлетворенный спрос на {unmet_demand} для типа машины {i + 1}.")
                self.inventory_levels[i] = 0


    
    def generate_clients(self, dig):
        """ Генерация матрицы расстояний между клиентами """
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
    
    
    def generation_customers_demand(self):
        """ Генерация спроса по каждому клиенту и суммарно """
        now_customer_amount = random.randint(3, self.dig - 2)

        numbers = list(range(self.dig))
    
        # Выбираем x случайных чисел из списка
        random_numbers = sorted(random.sample(numbers, now_customer_amount))
        # print(random_numbers)
        customers_demands = {}
        demands = [0] * self.num_car_types

        for i in range(now_customer_amount):
            demand = self.generate_demand()
            dict_demand = {index: value for index, value in enumerate(demand)}
            customers_demands[random_numbers[i]] = dict_demand
            demands = list(map(lambda a, b: a + b, demands, demand))

        return customers_demands, demands

    
    def call_routing(self, customers_demand):
        """ Вызов маршрутизации """
        # best = start_algorithm(self.clients_matrix)
        print(customers_demand)
        print(self.clients_matrix)
        best = cargo_distribution(customers_demand, self.clients_matrix)
        
        print(f"Стоимость пути: {best}")




    def simulate(self, time_period):
        """ Моделировать управление запасами за указанный период времени """
        for t in range(time_period):
            print("\n -------------------------------------")
            print(f"\nTime period {t + 1}:")
            # Генерация спроса
            customers_demand, demand = self.generation_customers_demand()

            print(f"Сгенерированный спрос: {demand}")
            
            # Обновление склада в соответствии со спросом
            self.update_inventory(demand)

            # Запуск маршрутизации
            self.call_routing(customers_demand)
            
            # Проверка уровня запасов
            orders = self.check_inventory()

            if orders:
                # Восполнение запасов
                self.place_orders(orders)

        print(f"\nОбщая сумма понесенных расходов: {self.total_cost}")





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
demand_means = [1, 1, 1, 1]
# Количество клиентов
dig = 10

# Инициализация стартовых параметров управления запасами
inventory_manager = InventoryManagement(num_car_types, 
                                        critical_levels, 
                                        pre_critical_levels,
                                        holding_costs, 
                                        order_costs, 
                                        demand_means,
                                        dig=dig)

# Вызов симуляции управления запасов на заданное количество месяцев
inventory_manager.simulate(12)