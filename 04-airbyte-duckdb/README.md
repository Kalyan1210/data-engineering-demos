# Airbyte to DuckDB Demo

A 10-minute demo showing how to set up data integration with Airbyte and build a data warehouse with DuckDB.

## 📊 Data Integration Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   External  │───▶│   Airbyte   │───▶│  Data       │───▶│  DuckDB     │
│   APIs      │    │  Connectors │    │  Processing │    │  Warehouse  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                    │
                          ▼                    ▼
                   ┌─────────────┐    ┌─────────────┐
                   │  Airbyte    │    │  Analytics  │
                   │  Web UI     │    │  Queries    │
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
cd 04-airbyte-duckdb

# Start Airbyte and DuckDB
docker-compose up -d

# Install dependencies
pip install duckdb pandas requests
```

### 2. Set Up DuckDB Warehouse
```bash
# Initialize DuckDB warehouse
python scripts/setup_duckdb.py
```

### 3. Run Data Replication
```bash
# Replicate data from APIs
python scripts/run_replication.py

# Query the warehouse
python scripts/query_warehouse.py
```

## 📊 What This Demo Shows

1. **Airbyte Setup**: Data integration platform
2. **DuckDB Warehouse**: Analytical database
3. **Data Replication**: Automated data pipelines
4. **API Integration**: Connecting to external data sources
5. **Analytics**: Querying and analyzing data

## 📁 Project Structure

```
scripts/
├── setup_duckdb.py      # DuckDB warehouse setup
├── run_replication.py   # Data replication from APIs
└── query_warehouse.py   # Analytics queries

data/
├── warehouse/           # DuckDB database files
├── raw/               # Raw data from APIs
└── processed/         # Processed data

configs/
└── airbyte/          # Airbyte configurations
```

## 🎯 Key Concepts Demonstrated

- **Data Integration**: Airbyte connectors for data sources
- **Data Warehousing**: DuckDB for analytical queries
- **ETL Pipeline**: Extract, Transform, Load process
- **API Integration**: Connecting to external services
- **Analytics**: SQL queries for data analysis

## 🔗 Service Access

- **Airbyte Web UI**: `http://localhost:3000`
  - Username: `airbyte`
  - Password: `password`
- **DuckDB**: Local filesystem
- **Airbyte API**: `http://localhost:8000`

## 🚀 Next Steps

1. Add more data sources
2. Implement incremental sync
3. Set up data quality checks
4. Add monitoring and alerting
5. Create automated pipelines

## 🐛 Troubleshooting

**Airbyte Issues**: Check container status
```bash
docker-compose ps
```

**DuckDB Issues**: Verify database files
```bash
ls -la data/warehouse/
```

**API Issues**: Check network connectivity
```bash
curl http://localhost:8000/health
``` 