from scipy.stats import poisson

demand_means = [1, 1, 1, 1]
for i in range(100):
    now_dem = [poisson.rvs(mu) for mu in demand_means]
    if sum(now_dem) == 0:
        print(now_dem)