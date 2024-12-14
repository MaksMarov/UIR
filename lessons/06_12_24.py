from asyncio import AbstractEventLoopPolicy
import random
from tkinter import Y
import matplotlib.pyplot as plt

n = 10000

x = [random.gauss() for _ in range(n)]
y = [random.random() * 5 for _ in range(n)]

plt.hist(x, alpha=0.5, bins = 20)
plt.hist(y, alpha=0.5, bins = 20)

plt.show()