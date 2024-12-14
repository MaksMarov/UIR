import random
import matplotlib.pyplot as plt
import math

a0 = 45
v0 = 12
g = 9.81
PI = 3.141526539

time = 500
n = 25

all_x = []
all_y = []

xs = []
indexes = []
avg_x = 0
avg_index = 0

for i in range(n):
    x = []
    y = []
    a = math.radians(a0 + random.randrange(-15, 15))
    v = v0 + random.random()
    for j in range(time):
        t = 0.1 * j
        xj = v * math.cos(a) * t
        yj = v * math.sin(a) * t - (g * t ** 2) / 2
        if yj <= 0 and t > 0:
            break
        x.append(xj)
        y.append(yj)
    all_x.append(x)
    all_y.append(y)

    xs.append(x[y.index(max(y))])
    indexes.append(y.index(max(y)))   

    plt.plot(x, y)
    
avg_x = int(sum(xs) / len(xs))
avg_index = int(sum(indexes) / len(indexes))

ys = []
for i in range(n):
    ys.append(all_y[i][avg_index])

plt.scatter([avg_x]*n, ys)
    
plt.show()

# Индекс среднего максимума Y
# Выборка по среднему индексу
# Средние значения