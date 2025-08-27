from manager import Manager
import time

m = Manager()

while True:
    try:
        m.consume()
        m.write_to_mongo()
    except Exception as e:
        print(f"Error in manager: {e}")
        time.sleep(10)