# Great Expectations with S3 Demo

A 10-minute demo showing how to set up data quality validation with Great Expectations and S3-compatible storage using MinIO.

## 📊 Data Quality Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Raw Data  │───▶│  Validation │───▶│  Great      │───▶│  Quality    │
│   (CSV)     │    │   Engine    │    │ Expectations │    │  Reports    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                    │
                          ▼                    ▼
                   ┌─────────────┐    ┌─────────────┐
                   │    MinIO    │    │  Validation │
                   │   (S3)      │    │   Results   │
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
cd 02-great-expectations-s3

# Start MinIO and Great Expectations
docker-compose up -d

# Install dependencies
pip install great-expectations boto3 pandas
```

### 2. Set Up Great Expectations
```bash
# Initialize Great Expectations
great_expectations init

# Configure S3 connection
python scripts/setup_ge.py
```

### 3. Run Data Quality Checks
```bash
# Generate sample data
python scripts/generate_data.py

# Create expectations
python scripts/create_expectations.py

# Validate data
python scripts/validate_data.py
```

## 📊 What This Demo Shows

1. **MinIO Setup**: S3-compatible object storage
2. **Great Expectations**: Data quality validation framework
3. **Expectation Creation**: Defining data quality rules
4. **Validation Pipeline**: Automated quality checks
5. **Quality Reports**: HTML reports with validation results

## 📁 Project Structure

```
data/
├── clean/            # Clean sample data
│   └── customers.csv
└── dirty/           # Data with quality issues
    └── customers_dirty.csv

scripts/
├── setup_ge.py      # Great Expectations setup
├── generate_data.py # Sample data generation
├── create_expectations.py
└── validate_data.py

notebooks/
└── data_quality_analysis.ipynb
```

## 🎯 Key Concepts Demonstrated

- **Data Quality**: Automated validation of data
- **Expectations**: Defining data quality rules
- **Validation**: Running quality checks
- **Reports**: HTML quality reports
- **S3 Integration**: Cloud storage compatibility

## 🔗 Service Access

- **MinIO Console**: `http://localhost:9001`
  - Username: `minioadmin`
  - Password: `minioadmin`
- **Great Expectations**: Local filesystem

## 🚀 Next Steps

1. Add more complex expectations
2. Set up automated validation
3. Integrate with CI/CD
4. Add alerting for failures
5. Create custom expectations

## 🐛 Troubleshooting

**MinIO Issues**: Check container status
```bash
docker-compose ps
```

**Great Expectations Issues**: Verify configuration
```bash
great_expectations --version
```

**Data Issues**: Check file permissions
```bash
ls -la data/
``` 