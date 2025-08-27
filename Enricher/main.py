from manager import Manager
import time

m = Manager()

while True:
    try:
        m.manage()
    except Exception as e:
        print(f"Error in manager: {e}")
        time.sleep(10)
