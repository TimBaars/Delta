import threading
import time

class StatusManager:
    def __init__(self, name="System"):
        self.SystemStatus = False
        self.lock = threading.Lock()
        self.name = name

    def check_current_status(self):
        self.lock.acquire(blocking=True, timeout=-1)
        returnVal = self.SystemStatus
        self.lock.release()
        return returnVal

    def check_status(self, status = False):
        print(f"{self.name}Status: {self.SystemStatus} - Checking for {status}")
        while True:
            self.lock.acquire(blocking=True, timeout=-1)
            currentStatus = self.SystemStatus
            self.lock.release()
            if (currentStatus == status):
                time.sleep(0.1)
            else:
                break

    def update_status(self, new_status):
        self.lock.acquire(blocking=True, timeout=-1)
        self.SystemStatus = new_status
        self.lock.release()
        print(f"{self.name}Status: {self.SystemStatus} - Updated status")
