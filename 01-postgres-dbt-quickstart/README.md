# Postgres + dbt Quick-Start Demo

A 10-minute demo showing how to set up a data warehouse with PostgreSQL and dbt, including seed data and basic transformations.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- pip

### 1. Start the Environment
```bash
# Clone and navigate to the demo
cd 01-postgres-dbt-quickstart

# Start PostgreSQL and pgAdmin
docker-compose up -d

# Install dbt
pip install dbt-postgres
```

### 2. Configure dbt
```bash
# Copy the profiles configuration
cp profiles.yml ~/.dbt/profiles.yml

# Edit the profiles file with your database credentials
# Default credentials are in docker-compose.yml
```

### 3. Run the Demo
```bash
# Initialize dbt project
dbt init postgres_demo

# Seed the data
dbt seed

# Run the models
dbt run

# Generate documentation
dbt docs generate
dbt docs serve
```

## 📊 What This Demo Shows

1. **PostgreSQL Setup**: Local database with pgAdmin interface
2. **dbt Project Structure**: Proper organization with staging and marts
3. **Seed Data**: Loading CSV files into the warehouse
4. **Transformations**: Building staging and dimensional models
5. **Documentation**: Auto-generated docs with dbt

## 📁 Project Structure

```
models/
├── staging/          # Raw data transformations
│   └── stg_customers.sql
└── marts/           # Business logic models
    └── dim_customers.sql

seeds/               # CSV files to load
└── raw_customers.csv
```

## 🎯 Key Concepts Demonstrated

- **Seeds**: Loading external CSV data
- **Staging Models**: Cleaning and standardizing raw data
- **Mart Models**: Business-ready dimensional models
- **dbt Run**: Executing the transformation pipeline
- **Documentation**: Auto-generated data lineage

## 🔗 Database Access

- **PostgreSQL**: `localhost:5432`
- **pgAdmin**: `http://localhost:8080`
  - Username: `admin@admin.com`
  - Password: `admin`

## 🚀 Next Steps

1. Add more complex transformations
2. Implement testing with dbt tests
3. Set up incremental models
4. Add data quality checks
5. Integrate with CI/CD pipeline

## 🐛 Troubleshooting

**Connection Issues**: Ensure Docker containers are running
```bash
docker-compose ps
```

**dbt Profile Issues**: Check your `~/.dbt/profiles.yml` configuration

**Permission Issues**: Make sure the scripts are executable
```bash
chmod +x scripts/*.sh
``` 