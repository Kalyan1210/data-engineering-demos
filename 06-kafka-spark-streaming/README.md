# Kafka + Spark Structured Streaming Demo

A 10-minute demo showing how to set up real-time data streaming with Apache Kafka and process it using Spark Structured Streaming.

## 📊 Streaming Data Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Data        │───▶│   Kafka     │───▶│ Spark       │───▶│ Processed   │
│ Generator   │    │   Broker    │    │ Streaming   │    │ Results     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                    │
                          ▼                    ▼
                   ┌─────────────┐    ┌─────────────┐
                   │ Kafka UI    │    │ Spark UI    │
                   │ (Port 8080) │    │ (Port 4040) │
                   └─────────────┘    └─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- pip

### 1. Start the Environment
```bash
# Navigate to the demo
cd 06-kafka-spark-streaming

# Start Kafka, Zookeeper, and Spark
docker-compose up -d

# Install dependencies
pip install pyspark kafka-python pandas
```

### 2. Start Data Generation
```bash
# Start Kafka producer to generate data
python scripts/produce_data.py
```

### 3. Start Spark Streaming
```bash
# Start Spark streaming job
python scripts/spark_streaming.py
```

### 4. View Results
- **Kafka UI**: `http://localhost:8080`
- **Spark UI**: `http://localhost:4040`
- **Jupyter Notebook**: `http://localhost:8888`

## 📁 Project Structure

```
app/
├── spark_streaming.py    # Spark structured streaming job
├── kafka_producer.py     # Kafka data producer
└── data_processor.py     # Data processing logic

scripts/
├── produce_data.py       # Data generation script
├── spark_streaming.py    # Spark streaming job
└── setup_kafka.py        # Kafka topic setup

configs/
├── spark-defaults.conf   # Spark configuration
└── kafka/
    └── server.properties # Kafka configuration

notebooks/
└── streaming_analysis.ipynb  # Jupyter notebook for analysis

docker-compose.yml        # Compose file for all services
README.md                 # This file
```

## 📊 What This Demo Shows

1. **Kafka Setup**: Message broker for real-time data streaming
2. **Spark Structured Streaming**: Real-time data processing
3. **Data Generation**: Simulated streaming data
4. **Stream Processing**: Windowed aggregations and transformations
5. **Real-time Analytics**: Live data processing and visualization

## 🎯 Key Concepts Demonstrated

- **Apache Kafka**: Distributed streaming platform
- **Spark Structured Streaming**: Real-time data processing
- **Stream Processing**: Windowed operations and aggregations
- **Data Pipelines**: End-to-end streaming architecture
- **Real-time Analytics**: Live data processing

## 🔗 Service Access

- **Kafka**: `localhost:9092`
- **Kafka UI**: `http://localhost:8080`
- **Spark UI**: `http://localhost:4040`
- **Jupyter**: `http://localhost:8888`

## 📈 Data Streams

- **User Events**: Page views, clicks, interactions
- **Sensor Data**: IoT device readings
- **Transaction Data**: Financial transactions
- **Log Data**: Application logs and metrics

## 🚀 Next Steps

1. Add more complex stream processing
2. Implement stateful operations
3. Add data quality checks
4. Set up monitoring and alerting
5. Integrate with data warehouses

## 🐛 Troubleshooting

**Kafka Issues**: Check container status
```bash
docker-compose ps
```

**Spark Issues**: Check Spark UI
```bash
curl http://localhost:4040
```

**Data Issues**: Verify Kafka topics
```bash
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092
``` 