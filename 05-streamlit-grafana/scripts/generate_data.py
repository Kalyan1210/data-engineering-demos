import time
from app.data_generator import generate_metrics

if __name__ == "__main__":
    while True:
        generate_metrics()
        print("Metrics updated.")
        time.sleep(2) 