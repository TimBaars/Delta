import threading
import time

class StatusManager:
    def __init__(self):
        self.SystemStatus = False
        self.lock = threading.Lock()

    def check_current_status(self, name="System"):
        self.name = name
        
        with self.lock:
            return self.SystemStatus

    def check_status(self, status = False):
        while self.check_current_status() == status:
            with self.lock:
                # print(f"{self.name}Status: {self.SystemStatus}")
                time.sleep(0.1)

    def update_status(self, new_status):
        with self.lock:
            self.SystemStatus = new_status
