# Great Expectations with S3 Demo

A 10-minute demo showing how to set up data quality validation using Great Expectations with MinIO (S3-compatible storage).

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

# Install Great Expectations
pip install great-expectations
```

### 2. Initialize Great Expectations
```bash
# Initialize Great Expectations project
great_expectations init

# Configure MinIO as a data source
python scripts/setup_gx.py
```

### 3. Run the Demo
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
3. **Sample Data**: CSV files with various data quality issues
4. **Expectations**: Data quality rules and validations
5. **Validation Results**: Automated data quality reports

## 📁 Project Structure

```
data/                    # Sample CSV files
├── clean_data.csv      # Valid data
└── dirty_data.csv      # Data with quality issues

expectations/            # Great Expectations configs
└── ge_config/

notebooks/              # Jupyter notebooks
└── data_quality_analysis.ipynb

scripts/                # Automation scripts
├── setup_gx.py
├── generate_data.py
├── create_expectations.py
└── validate_data.py
```

## 🎯 Key Concepts Demonstrated

- **Data Quality**: Validating data integrity and consistency
- **Great Expectations**: Modern data quality framework
- **S3 Storage**: Cloud-native data storage
- **Automated Validation**: CI/CD for data quality
- **Expectation Suites**: Reusable validation rules

## 🔗 Service Access

- **MinIO Console**: `http://localhost:9001`
  - Username: `minioadmin`
  - Password: `minioadmin`
- **Great Expectations Docs**: `http://localhost:8080`

## 🚀 Next Steps

1. Add more complex data quality rules
2. Integrate with CI/CD pipelines
3. Set up automated alerts
4. Create custom expectations
5. Add data profiling

## 🐛 Troubleshooting

**MinIO Connection Issues**: Ensure containers are running
```bash
docker-compose ps
```

**Great Expectations Issues**: Check the configuration
```bash
great_expectations --version
```

**Data Validation Issues**: Check the sample data format
```bash
head -5 data/clean_data.csv
``` 