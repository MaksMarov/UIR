import random

class Channel():
    def __init__(self, processing_time, number):
        self.number = number
        self.base_processing_time = processing_time
        self.current_processing_time = self.base_processing_time
        self.request = None
        self.done_requests = []
        self.busy_time = 0
        self.time = 0
        
    def is_busy(self):
        return True if self.request else False
    
    def take_request(self, request):
        if request:
            self.request = request
            self.current_processing_time = int(self.base_processing_time * random.uniform(0.9, 1.1))
            print(f"Channel #{self.number} processing the request number {self.request.number}")
        else:
            print(f"Incorrect request! Request = {request}, Channel = {self.number}")
            
    def processing(self):
        if self.is_busy():
            if self.time >= self.current_processing_time:
                self.finish_request()
                self.busy_time += self.time
                self.time = 0
            else:
                self.time += 1
                
    def finish_request(self):
        self.done_requests.append(self.request)
        self.request = None
        print(f"Channel #{self.number} has finished processing the request")
        
    def get_average__processing_intensity(self):
        return (self.busy_time / len(self.done_requests)) if self.done_requests > 0 else 0