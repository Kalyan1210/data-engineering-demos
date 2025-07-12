# FastAPI + MLflow Tracking Demo

A 10-minute demo showing how to build a FastAPI application with MLflow for model tracking and serving.

## 📊 ML Pipeline Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Training    │───▶│  MLflow     │───▶│  FastAPI    │───▶│  Model      │
│ Data        │    │  Tracking   │    │  Server     │    │  Serving    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                    │
                          ▼                    ▼
                   ┌─────────────┐    ┌─────────────┐
                   │  MLflow UI  │    │  API Docs   │
                   │  (Port 5000)│    │  (Port 8000)│
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
cd 03-fastapi-mlflow

# Start MLflow and PostgreSQL
docker-compose up -d

# Install dependencies
pip install fastapi uvicorn mlflow scikit-learn pandas
```

### 2. Train and Track Models
```bash
# Generate sample data
python scripts/generate_data.py

# Train models with MLflow tracking
python scripts/train_models.py
```

### 3. Start the FastAPI Server
```bash
# Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 What This Demo Shows

1. **FastAPI Setup**: Modern Python web framework
2. **MLflow Tracking**: Model experiment tracking
3. **Model Training**: Automated model training pipeline
4. **API Serving**: RESTful model serving
5. **Experiment Management**: MLflow UI for experiments

## 📁 Project Structure

```
app/
├── main.py           # FastAPI application
├── models.py         # ML model definitions
└── schemas.py        # Pydantic schemas

scripts/
├── generate_data.py  # Sample data generation
└── train_models.py   # Model training script

notebooks/
└── model_experiments.ipynb

data/
└── training_data.csv
```

## 🎯 Key Concepts Demonstrated

- **FastAPI**: Modern async web framework
- **MLflow Tracking**: Experiment tracking and model registry
- **Model Serving**: RESTful API for model predictions
- **Data Validation**: Pydantic schemas for API validation
- **Experiment Management**: MLflow UI for experiment tracking

## 🔗 Service Access

- **FastAPI**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`
- **MLflow UI**: `http://localhost:5000`
- **PostgreSQL**: `localhost:5432`

## 🚀 Next Steps

1. Add model versioning
2. Implement A/B testing
3. Add model monitoring
4. Set up automated retraining
5. Add authentication

## 🐛 Troubleshooting

**MLflow Issues**: Check container status
```bash
docker-compose ps
```

**FastAPI Issues**: Check server logs
```bash
uvicorn app.main:app --reload --log-level debug
```

**Model Issues**: Verify MLflow tracking
```bash
mlflow ui --port 5000
``` 