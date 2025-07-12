from prometheus_client import Counter, Gauge

page_views = Counter('page_views', 'Number of page views')
records_processed = Counter('records_processed', 'Records processed')
processing_time = Gauge('processing_time', 'Processing time in ms')
cpu_usage = Gauge('cpu_usage', 'CPU usage percent')
memory_usage = Gauge('memory_usage', 'Memory usage in MB') 