# Superset + SQLite Demo

A 10-minute demo showing how to set up Apache Superset for business intelligence and data visualization with SQLite as the data source.

## 📊 BI Data Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Sample      │───▶│   SQLite    │───▶│  Superset   │───▶│ Dashboards  │
│ Data        │    │   Database  │    │   BI Tool   │    │ & Charts    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                    │
                          ▼                    ▼
                   ┌─────────────┐    ┌─────────────┐
                   │ Data        │    │  Charts &   │
                   │ Exploration │    │  Analytics  │
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
cd 07-superset-sqlite

# Start Superset and SQLite
docker-compose up -d

# Install dependencies
pip install apache-superset sqlite3 pandas
```

### 2. Initialize Superset
```bash
# Initialize Superset database
python scripts/init_superset.py

# Create admin user
python scripts/create_admin.py
```

### 3. Load Sample Data
```bash
# Generate and load sample data
python scripts/load_data.py
```

### 4. Access Superset
- **Superset**: `http://localhost:8088`
  - Username: `admin`
  - Password: `admin`

## 📁 Project Structure

```
app/
├── data_generator.py    # Sample data generation
├── database_setup.py    # SQLite database setup
└── superset_config.py   # Superset configuration

scripts/
├── init_superset.py     # Superset initialization
├── create_admin.py      # Admin user creation
├── load_data.py         # Data loading script
└── setup_dashboards.py  # Dashboard setup

data/
├── sample_data.csv      # Sample business data
└── database/
    └── business.db      # SQLite database

configs/
├── superset_config.py   # Superset configuration
└── sqlite/
    └── schema.sql       # Database schema

notebooks/
└── data_analysis.ipynb  # Jupyter notebook for analysis

docker-compose.yml        # Compose file for all services
README.md                 # This file
```

## 📊 What This Demo Shows

1. **Superset Setup**: Apache Superset BI platform
2. **SQLite Database**: Lightweight data storage
3. **Sample Data**: Business metrics and KPIs
4. **Data Visualization**: Charts, dashboards, and analytics
5. **Business Intelligence**: Interactive data exploration

## 🎯 Key Concepts Demonstrated

- **Apache Superset**: Modern BI and data visualization platform
- **SQLite**: Lightweight relational database
- **Data Visualization**: Charts, graphs, and dashboards
- **Business Intelligence**: Interactive data exploration
- **SQL Analytics**: Complex queries and aggregations

## 🔗 Service Access

- **Superset**: `http://localhost:8088`
  - Username: `admin`
  - Password: `admin`
- **SQLite**: Local database files

## 📈 Sample Data

- **Sales Data**: Revenue, products, regions
- **Customer Data**: Demographics, behavior, segments
- **Product Data**: Categories, prices, inventory
- **Time Series**: Monthly trends and patterns

## 🚀 Next Steps

1. Add more complex data models
2. Create advanced dashboards
3. Set up automated data refresh
4. Add user roles and permissions
5. Integrate with external data sources

## 🐛 Troubleshooting

**Superset Issues**: Check container status
```bash
docker-compose ps
```

**Database Issues**: Verify SQLite file
```bash
ls -la data/database/
```

**Access Issues**: Check Superset logs
```bash
docker-compose logs superset
``` 