import numpy as np
from metrics import page_views, records_processed, processing_time, cpu_usage, memory_usage

def generate_metrics():
    page_views.inc(np.random.randint(1, 5))
    records_processed.inc(np.random.randint(10, 100))
    processing_time.set(np.random.uniform(50, 500))
    cpu_usage.set(np.random.uniform(5, 90))
    memory_usage.set(np.random.uniform(100, 8000)) 