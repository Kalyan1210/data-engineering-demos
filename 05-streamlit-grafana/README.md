# Streamlit → Grafana Demo

A 10-minute demo showing how to build a Streamlit app that generates metrics and pushes them to Prometheus for visualization in Grafana.

## 📊 Data Flow Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Streamlit   │───▶│ Prometheus  │───▶│ Grafana     │───▶│ Dashboards  │
│ App         │    │ Metrics DB  │    │ Visualization│    │ & Alerts    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- pip

### 1. Start the Environment
```bash
# Navigate to the demo
cd 05-streamlit-grafana

# Start Prometheus and Grafana
docker-compose up -d

# Install dependencies
pip install streamlit prometheus-client pandas numpy
```

### 2. Start the Streamlit App
```bash
# Start the Streamlit application
streamlit run app/main.py --server.port 8501
```

### 3. View Dashboards
- **Streamlit App**: `http://localhost:8501`
- **Grafana**: `http://localhost:3000`
  - Username: `admin`
  - Password: `admin`

## 📁 Project Structure

```
app/
├── main.py           # Main Streamlit app
├── metrics.py        # Prometheus metrics
├── data_generator.py # Sample data generation
├── requirements.txt  # Python dependencies
├── Dockerfile        # Streamlit app Dockerfile

configs/
├── prometheus.yml    # Prometheus configuration
└── grafana/
    ├── datasources.yml      # Grafana data source provisioning
    └── sample_dashboard.json# Sample dashboard

scripts/
├── setup_grafana.py  # Grafana dashboard setup
└── generate_data.py  # Data generation script

notebooks/
└── metrics_analysis.ipynb   # Jupyter notebook for metrics analysis

docker-compose.yml    # Compose file for all services
README.md             # This file
```

## 📈 Metrics Generated

- **User Activity**: Page views, interactions
- **Data Processing**: Records processed, processing time
- **System Performance**: CPU usage, memory usage

## 🎯 Key Concepts Demonstrated

- **Streamlit**: Modern Python web framework for data apps
- **Prometheus**: Time-series metrics database
- **Grafana**: Data visualization platform
- **Real-time Monitoring**: Live metric collection
- **Custom Dashboards**: Building visualizations

## 🔗 Service Access

- **Streamlit App**: `http://localhost:8501`
- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3000`
  - Username: `admin`
  - Password: `admin`

## 🚀 Next Steps

1. Add more complex metrics
2. Implement alerting rules
3. Set up automated dashboards
4. Add data source integrations
5. Configure notification systems

## 🐛 Troubleshooting

**Prometheus Issues**: Check container status
```bash
docker-compose ps
```

**Grafana Issues**: Verify dashboard configuration
```bash
curl http://localhost:3000/api/health
```

**Streamlit Issues**: Check app logs
```bash
streamlit run app/main.py --server.port 8501 --logger.level debug
``` 