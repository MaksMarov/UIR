import random
import matplotlib.pyplot as plt

n = 100

def fx_1(i):
    f = i + 10
    return min(max(0, f), 100)

def fy_1(i):
    f = random.random() * 2e6
    f = i * random.random() / 100 * 2e6
    return min(max(1e6, f), 2e6)

def fx_2(i):
    f = int((i * 5 - 2) / 5)
    return min(max(1, f), 100)

def fy_2(i):
    f = i - 50 > 0
    return 0 if f else 1
    # return random.choice([0, 1])

x1 = [fx_1(i) for i in range(n)]
x2 = [fx_2(i) for i in range(n)]

y1 = [fy_1(x1[i]) for i in range(n)]
y2 = [fy_2(x2[i]) for i in range(n)]

avg_x1 = sum(x1) / n
avg_y1 = sum(y1) / n

x1_diffs = [xi - avg_x1 for xi in x1]
y1_diffs = [yi - avg_y1 for yi in y1]

avg_x2 = sum(x2) / n
avg_y2 = sum(y2) / n

x2_diffs = [xi - avg_x2 for xi in x2]
y2_diffs = [yi - avg_y2 for yi in y2]

product1 = [x1_diffs[i] * y1_diffs[i] for i in range(n)]
cov1 = sum(product1) / n

sx1 = (sum(xi ** 2 for xi in x1_diffs) / n) ** (1/2)
sy1 = (sum(yi ** 2 for yi in y1_diffs) / n) ** (1/2)

r1 = cov1 / (sx1 * sy1)

print(x1, y1)

print(cov1, r1)

plt.scatter(x1, y1)
plt.show()



product2 = [x2_diffs[i] * y2_diffs[i] for i in range(n)]
cov2 = sum(product2) / n

sx2 = (sum(xi ** 2 for xi in x2_diffs) / n) ** (1/2)
sy2 = (sum(yi ** 2 for yi in y2_diffs) / n) ** (1/2)

r2 = cov2 / (sx2 * sy2)

print(x2, y2)

print(cov2, r2)

plt.scatter(x2, y2)
plt.show()
