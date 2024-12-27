from Lab4.smo import SMO
import matplotlib.pyplot as plt

russka_pochta = SMO(channels_count=5, lam=0.5, mu=0.8, shift_time=1000)
russka_pochta.start_shift()
data = russka_pochta.get_components_data()
print(data)

plt.scatter([i for i in range(data.channel_count)], data.busy_times )
plt.ylim(0, max(data.busy_times) + 4)
plt.show()