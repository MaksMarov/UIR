import random

class Request():
    def __init__(self, num):
        self.number = num
        self.waiting_time = 0

    def waiting(self):
        self.waiting_time += 1

class Queue():
    def __init__(self, request_generation_time):
        self.requests = []
        self.base_request_generation_time = request_generation_time
        self.current_request_generation_time = self.base_request_generation_time
        self.time = 0
        self.work_time = 0
        self.received_requests = 0
        
    def is_empty(self):
        return len(self.requests) > 0

    def update(self):
        for request in self.requests:
            request.waiting()
            
        if self.time >= self.current_request_generation_time:
            self.new_request()
            self.work_time += self.time
            self.time = 0
        else:
            self.time += 1
            
    def new_request(self):
        self.received_requests += 1
        self.requests.append(Request(self.received_requests))
        self.current_request_generation_time = int(self.base_request_generation_time * random.uniform(0.9, 1.1))
        
    def get_next_request(self):
        if len(self.requests) > 0:
            request = min(self.requests, key=lambda x: x.number)
            self.requests.remove(request)
            return request
        else:
            print("Queue is empty")
            return None
        
    def get_avg_rgen_time(self):
        return (self.work_time / self.received_requests) if self.received_requests > 0 else 0