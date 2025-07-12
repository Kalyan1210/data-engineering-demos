# Dagster Data Assets Demo

A 10-minute demo showing how to set up Dagster for data asset management, pipeline orchestration, and data lineage tracking with modern data engineering practices.

## 🏗️ Data Asset Management Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Raw Data    │───▶│ Data Assets │───▶│ Pipelines   │───▶│ Data Lineage│
│ Sources     │    │ Management  │    │ Orchestration│    │ & Tracking  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                    │
                          ▼                    ▼
                   ┌─────────────┐    ┌─────────────┐
                   │ Asset       │    │  Dependency │
                   │ Dependencies│    │  Graphs     │
                   └─────────────┘    └─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Docker (optional)

### 1. Install Dagster
```bash
# Navigate to the demo
cd 09-dagster-data-assets

# Install Dagster
pip install dagster dagster-webserver dagster-postgres

# Install additional dependencies
pip install pandas numpy sqlalchemy psycopg2-binary
```

### 2. Start Dagster
```bash
# Start Dagster webserver
dagster dev

# Or use Docker Compose
docker-compose up -d
```

### 3. Run Sample Assets
```bash
# Run data assets pipeline
python assets/data_assets.py

# Run ETL assets pipeline
python assets/etl_assets.py

# Run analytics assets pipeline
python assets/analytics_assets.py
```

### 4. Access Dagster UI
- **Dagster UI**: `http://localhost:3000`
- **API**: `http://localhost:3000/graphql`

## 📁 Project Structure

```
assets/
├── data_assets.py        # Basic data assets
├── etl_assets.py         # ETL asset pipeline
├── analytics_assets.py   # Analytics asset pipeline
└── utils/
    ├── data_processor.py # Data processing utilities
    ├── db_connector.py   # Database connection utilities
    └── validators.py     # Data validation utilities

definitions/
├── __init__.py           # Dagster definitions
├── data_assets.py        # Data asset definitions
├── etl_assets.py         # ETL asset definitions
└── analytics_assets.py   # Analytics asset definitions

configs/
├── dagster.yaml         # Dagster configuration
└── assets/
    ├── data_assets.yaml     # Data asset configuration
    ├── etl_assets.yaml      # ETL asset configuration
    └── analytics_assets.yaml # Analytics asset configuration

data/
├── raw/                 # Raw data files
├── processed/           # Processed data files
├── analytics/           # Analytics outputs
└── logs/               # Pipeline logs

scripts/
├── setup_dagster.py     # Dagster setup script
├── run_assets.py        # Asset runner script
└── monitor_assets.py    # Asset monitoring script

notebooks/
└── asset_analysis.ipynb # Jupyter notebook for analysis

docker-compose.yml        # Compose file for all services
README.md                 # This file
```

## 🏗️ What This Demo Shows

1. **Dagster Setup**: Local deployment and configuration
2. **Data Assets**: Asset management and dependencies
3. **Pipeline Orchestration**: Asset-based pipeline execution
4. **Data Lineage**: Asset dependency tracking
5. **Monitoring**: Real-time asset monitoring and observability

## 🎯 Key Concepts Demonstrated

- **Dagster**: Modern data orchestration platform
- **Data Assets**: Declarative data asset management
- **Asset Dependencies**: Automatic dependency resolution
- **Data Lineage**: End-to-end data flow tracking
- **Pipeline Orchestration**: Asset-based pipeline execution

## 🔗 Service Access

- **Dagster UI**: `http://localhost:3000`
- **GraphQL API**: `http://localhost:3000/graphql`
- **Asset Logs**: Local file system

## 📊 Sample Assets

- **Data Assets**: Raw data ingestion and validation
- **ETL Assets**: Data transformation and processing
- **Analytics Assets**: Business intelligence and reporting
- **Monitoring Assets**: Data quality and health checks

## 🚀 Next Steps

1. Add more complex asset dependencies
2. Set up external asset sources
3. Configure asset materialization
4. Add data quality checks
5. Integrate with external systems

## 🐛 Troubleshooting

**Dagster Issues**: Check server status
```bash
dagster dev --package-name assets
```

**Asset Issues**: Check asset logs
```bash
dagster asset materialize --select data_assets
```

**Connection Issues**: Verify configuration
```bash
dagster config validate
``` 