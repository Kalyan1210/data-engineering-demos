# Airbyte to DuckDB Demo

A 10-minute demo showing how to replicate data from a public API into a local DuckDB data warehouse using Airbyte.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- pip

### 1. Start the Environment
```bash
# Navigate to the demo
cd 04-airbyte-duckdb

# Start Airbyte and DuckDB services
docker-compose up -d

# Install dependencies
pip install duckdb pandas requests
```

### 2. Set Up Airbyte
```bash
# Wait for Airbyte to be ready (check http://localhost:8000)
# Default credentials: airbyte / password

# Configure source and destination
python scripts/setup_airbyte.py
```

### 3. Run Data Replication
```bash
# Start data replication
python scripts/run_replication.py

# Query the data warehouse
python scripts/query_warehouse.py
```

## 📊 What This Demo Shows

1. **Airbyte Setup**: Modern data integration platform
2. **DuckDB**: Fast analytical database
3. **API Integration**: Replicating data from public APIs
4. **Data Transformation**: ETL/ELT pipeline setup
5. **Query Interface**: SQL queries on replicated data

## 📁 Project Structure

```
data/                    # Sample data and outputs
├── raw/                # Raw data from APIs
├── processed/          # Transformed data
└── warehouse/          # DuckDB database files

configs/                # Airbyte configurations
├── sources/           # Source connector configs
└── destinations/      # Destination configs

scripts/               # Automation scripts
├── setup_airbyte.py   # Airbyte configuration
├── run_replication.py # Data replication
└── query_warehouse.py # Query examples

notebooks/             # Jupyter notebooks
└── data_analysis.ipynb
```

## 🎯 Key Concepts Demonstrated

- **Data Integration**: Airbyte for ETL/ELT pipelines
- **Analytical Database**: DuckDB for fast analytics
- **API Replication**: Extracting data from external sources
- **Data Transformation**: Processing and cleaning data
- **SQL Analytics**: Querying replicated data

## 🔗 Service Access

- **Airbyte UI**: `http://localhost:8000`
  - Username: `airbyte`
  - Password: `password`
- **DuckDB**: Local database files
- **API Endpoints**: Various public APIs

## 🚀 Data Sources

- **Weather API**: Current weather data
- **Stock API**: Financial market data
- **News API**: Recent news articles
- **User Data**: Sample user profiles

## 🚀 Next Steps

1. Add more data sources
2. Implement incremental sync
3. Set up data quality checks
4. Add automated scheduling
5. Integrate with BI tools

## 🐛 Troubleshooting

**Airbyte Connection Issues**: Ensure containers are running
```bash
docker-compose ps
```

**DuckDB Issues**: Check database file permissions
```bash
ls -la data/warehouse/
```

**API Issues**: Verify API endpoints and keys
```bash
python scripts/test_apis.py
``` 