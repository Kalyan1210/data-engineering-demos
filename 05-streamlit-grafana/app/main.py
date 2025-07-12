import streamlit as st
import time
from prometheus_client import start_http_server
from metrics import page_views, records_processed, processing_time, cpu_usage, memory_usage
from data_generator import generate_metrics
import threading

st.set_page_config(page_title="Streamlit → Grafana Demo", layout="wide")
st.title("Streamlit → Grafana Demo")

# Start Prometheus metrics server in a background thread
PROMETHEUS_PORT = 8000

def run_prometheus_server():
    start_http_server(PROMETHEUS_PORT)

threading.Thread(target=run_prometheus_server, daemon=True).start()

# Simulate metrics update in the background
def update_metrics():
    while True:
        generate_metrics()
        time.sleep(2)

threading.Thread(target=update_metrics, daemon=True).start()

# Streamlit UI
tabs = st.tabs(["Live Metrics", "About"])

with tabs[0]:
    st.metric("Page Views", page_views._value.get())
    st.metric("Records Processed", records_processed._value.get())
    st.metric("Processing Time (ms)", round(processing_time._value.get(), 2))
    st.metric("CPU Usage (%)", round(cpu_usage._value.get(), 2))
    st.metric("Memory Usage (MB)", round(memory_usage._value.get(), 2))
    st.write("Metrics are updated every 2 seconds and available at :8000/metrics for Prometheus.")

with tabs[1]:
    st.markdown("""
    - **Streamlit** generates and displays metrics
    - **Prometheus** scrapes metrics from `/metrics`
    - **Grafana** visualizes metrics in real time
    """) 