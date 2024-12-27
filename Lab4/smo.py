from Lab4.channel import Channel
from Lab4.request import Queue
from Lab4.data import ComponentsData

import random

class SMO():
    def __init__(self, channels_count, lam, mu, shift_time):
        self.shift_time = shift_time
        self.lam = lam
        self.t_lam = int(1 / lam)
        self.mu = mu
        self.t_mu = int(1 / mu)
        self.channels = [Channel(self.t_mu, number=i) for i in range(channels_count)]
        self.queue = Queue(self.t_lam)

    def start_shift(self):
        print("The shift has begun")
        for _ in range(self.shift_time):
            for channel in self.channels:
                channel.processing()
                
            self.queue.update()
            if not self.queue.is_empty():
                free_channels = [channel for channel in self.channels if not channel.is_busy()]
                # free_channel = free_channels[0] if free_channels else None
                free_channel = random.choice(free_channels) if free_channels else None
                if free_channel:
                    free_channel.take_request(self.queue.get_next_request())

        print("The working day is over. Working overtime...")
        
        while any(channel.is_busy() for channel in self.channels):
            for channel in self.channels:
                channel.processing()
        print("Shift's over")
        

    def collect_all_requests(self):
        all_requests = []
        for channel in self.channels:
            all_requests.extend(channel.done_requests)
        return all_requests
        
    def get_components_data(self):
        busy_times = [channel.busy_time for channel in self.channels]
        requests = self.collect_all_requests()
        requests_waiting_times = [request.waiting_time for request in requests]
        processing_times = [channel.get_average_processing_intensity() for channel in self.channels]
        avg_processing_time = (sum(processing_times) / len(processing_times)) if processing_times else 0
        real_mu = (1 / avg_processing_time) if avg_processing_time else 0
        avg_rgen_time = self.queue.get_avg_rgen_time()
        real_lam = (1 / avg_rgen_time) if avg_rgen_time else 0
        no_taken_requests = len(self.queue.requests)
    
        return ComponentsData(self.mu, self.lam, real_mu, real_lam, busy_times, requests_waiting_times, no_taken_requests)