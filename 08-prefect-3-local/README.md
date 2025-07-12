# Prefect 3 Local Deployment Demo

A 10-minute demo showing how to set up Prefect 3 for workflow orchestration with local deployment, including data pipelines, monitoring, and scheduling.

## 🔄 Workflow Orchestration Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Data        │───▶│ Prefect     │───▶│ Workflow    │───▶│ Monitoring  │
│ Sources     │    │ Orchestrator│    │ Execution   │    │ & Logging   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                    │
                          ▼                    ▼
                   ┌─────────────┐    ┌─────────────┐
                   │ Task        │    │  Schedules  │
                   │ Management  │    │ & Triggers  │
                   └─────────────┘    └─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Docker (optional)

### 1. Install Prefect
```bash
# Navigate to the demo
cd 08-prefect-3-local

# Install Prefect 3
pip install prefect

# Install additional dependencies
pip install pandas requests sqlalchemy
```

### 2. Start Prefect Server
```bash
# Start Prefect server locally
prefect server start

# Or use Docker Compose
docker-compose up -d
```

### 3. Run Sample Workflows
```bash
# Run data pipeline workflow
python workflows/data_pipeline.py

# Run ETL workflow
python workflows/etl_workflow.py

# Run scheduled workflow
python workflows/scheduled_workflow.py
```

### 4. Access Prefect UI
- **Prefect UI**: `http://localhost:4200`
- **API**: `http://localhost:4200/api`

## 📁 Project Structure

```
workflows/
├── data_pipeline.py      # Basic data pipeline
├── etl_workflow.py       # ETL workflow with transformations
├── scheduled_workflow.py # Scheduled workflow example
└── utils/
    ├── data_processor.py # Data processing utilities
    ├── db_connector.py   # Database connection utilities
    └── validators.py     # Data validation utilities

configs/
├── prefect.yaml         # Prefect configuration
└── workflows/
    ├── data_pipeline.yaml    # Pipeline configuration
    ├── etl_workflow.yaml     # ETL configuration
    └── scheduled_workflow.yaml # Schedule configuration

data/
├── raw/                 # Raw data files
├── processed/           # Processed data files
└── logs/               # Workflow logs

scripts/
├── setup_prefect.py     # Prefect setup script
├── run_workflows.py     # Workflow runner script
└── monitor_workflows.py # Monitoring script

notebooks/
└── workflow_analysis.ipynb  # Jupyter notebook for analysis

docker-compose.yml        # Compose file for all services
README.md                 # This file
```

## 🔄 What This Demo Shows

1. **Prefect 3 Setup**: Local deployment and configuration
2. **Workflow Orchestration**: Task management and dependencies
3. **Data Pipelines**: ETL processes and transformations
4. **Scheduling**: Automated workflow execution
5. **Monitoring**: Real-time workflow tracking and logging

## 🎯 Key Concepts Demonstrated

- **Prefect 3**: Modern workflow orchestration platform
- **Task Management**: Dependency management and execution
- **Data Pipelines**: ETL and data processing workflows
- **Scheduling**: Automated workflow triggers
- **Monitoring**: Real-time workflow observability

## 🔗 Service Access

- **Prefect UI**: `http://localhost:4200`
- **Prefect API**: `http://localhost:4200/api`
- **Workflow Logs**: Local file system

## 📊 Sample Workflows

- **Data Pipeline**: Extract, transform, and load data
- **ETL Workflow**: Complex data transformations
- **Scheduled Workflow**: Automated data processing
- **Monitoring Workflow**: Health checks and alerts

## 🚀 Next Steps

1. Add more complex workflows
2. Set up external triggers
3. Configure notifications
4. Add data quality checks
5. Integrate with external systems

## 🐛 Troubleshooting

**Prefect Server Issues**: Check server status
```bash
prefect server status
```

**Workflow Issues**: Check logs
```bash
prefect logs
```

**Connection Issues**: Verify configuration
```bash
prefect config view
``` 