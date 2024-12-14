import random
import matplotlib.pyplot as plt

n = 100

x = [i for i in range(n)]
y = [4 * xi + 50 * random.random() for xi in x]

avg_x = sum(x) / n
avg_y = sum(y) / n

x_diffs = [xi - avg_x for xi in x]
y_diffs = [yi - avg_y for yi in y]

product = [x_diffs[i] * y_diffs[i] for i in range(n)]
cov = sum(product) / n

sx = (sum(xi ** 2 for xi in x_diffs) / n) ** (1/2)
sy = (sum(yi ** 2 for yi in y_diffs) / n) ** (1/2)

r = cov / (sx * sy)

print(cov, r)

plt.scatter(x, y)
plt.show()