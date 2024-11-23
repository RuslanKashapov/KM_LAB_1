
import random

dig = 20

now_customer_amount = random.randint(3, dig - 2)

numbers = list(range(dig))

# Выбираем x случайных чисел из списка
random_numbers = sorted(random.sample(numbers, now_customer_amount))

print(random_numbers)

# for i in range(now_customer_amount)

