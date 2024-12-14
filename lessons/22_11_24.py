import random
from urllib import request
import matplotlib.pyplot as plt

class Channel():
    def __init__(self, mu, number):
        self.number = number
        self.mu = mu
        self.next_free_time = 0
        self.is_busy = False
        self.busy_time = 0
        
    def __repr__(self):
        return f"{self.number}, t = {self.next_free_time}"

class SMO():
    def __init__(self, channels_count, requests_count, lam, mu):
        self.requests_count = requests_count
        self.lam = lam # Кол-во заявок в единицу времени
        self.t_lam = int(1 / lam)
        self.mu = mu # Кол-во обрабатываемых заявок в единицу времени
        self.t_mu = int(1 / mu)
        self.channels = [Channel(self.mu, i) for i in range(channels_count)]
        self.generate_requests()
        self.no_taken = 0
        
    def generate_requests(self):
        self.requests = [0]
        for i in range(self.requests_count):
            self.requests.append(self.requests[-1] + random.randrange(self.t_lam - 1, self.t_lam + 1))
            self.shift_time = self.requests[-1] + self.t_mu + 1
        print(f"Requests time: {self.requests}")
            
    def start_shift(self):
        for time in range(self.shift_time + 1):
            print(f"Time : {time}")
            if time in self.requests:
                print(f"Gor request! Time : {time}")
                is_taken = False
                free_channels = [channel for channel in self.channels if not channel.is_busy]
                if free_channels:
                    chosen_channel = free_channels[0]
                    t_mu = random.randrange(self.t_mu - 1, self.t_mu + 1)
                    chosen_channel.next_free_time = time + t_mu
                    chosen_channel.busy_time += t_mu
                    chosen_channel.is_busy = True
                    print(f"Request was taken by channel{chosen_channel}. ")
                else:
                    self.no_taken += 1
                    print(f"Request {time} was no taken")
            for channel in self.channels:
                if channel.next_free_time == time:
                    channel.next_free_time = 0
                    channel.is_busy = False
        print(self.no_taken)
        busy_time = [channel.busy_time for channel in self.channels]
        plt.scatter([i for i in range(len(self.channels))], busy_time )
        plt.ylim(0, max(busy_time) + 4)
        
        
# random.seed(1)
pyaterochka = SMO(5, 15, 1/2, 1/8)
pyaterochka.start_shift()
plt.show()

#Делаем с очередью