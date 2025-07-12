# FastAPI + MLflow Tracking Demo

A 10-minute demo showing how to build a machine learning API with FastAPI and track experiments using MLflow.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- pip

### 1. Start the Environment
```bash
# Navigate to the demo
cd 03-fastapi-mlflow

# Start MLflow and FastAPI services
docker-compose up -d

# Install dependencies
pip install fastapi uvicorn mlflow scikit-learn pandas numpy
```

### 2. Train and Track Models
```bash
# Train a sample model with MLflow tracking
python scripts/train_model.py

# View experiments in MLflow UI
# Open http://localhost:5000
```

### 3. Start the FastAPI Server
```bash
# Start the FastAPI application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API will be available at http://localhost:8000
# Documentation at http://localhost:8000/docs
```

## 📊 What This Demo Shows

1. **FastAPI Setup**: Modern Python web framework for APIs
2. **MLflow Tracking**: Experiment tracking and model versioning
3. **Model Training**: Sample ML pipeline with scikit-learn
4. **API Endpoints**: RESTful API for model predictions
5. **Experiment Management**: MLflow UI for experiment tracking

## 📁 Project Structure

```
app/                    # FastAPI application
├── main.py            # FastAPI app entry point
├── models.py          # ML model utilities
└── schemas.py         # Pydantic schemas

models/                 # Trained models
└── model_registry/

data/                   # Sample datasets
├── train.csv          # Training data
└── test.csv           # Test data

notebooks/             # Jupyter notebooks
└── model_experiments.ipynb

scripts/               # Automation scripts
├── train_model.py     # Model training script
├── generate_data.py   # Data generation
└── evaluate_model.py  # Model evaluation
```

## 🎯 Key Concepts Demonstrated

- **FastAPI**: Modern, fast web framework for APIs
- **MLflow Tracking**: Experiment tracking and model management
- **Model Versioning**: Version control for ML models
- **RESTful APIs**: Clean API design with automatic docs
- **Experiment Management**: Reproducible ML experiments

## 🔗 Service Access

- **FastAPI**: `http://localhost:8000`
- **FastAPI Docs**: `http://localhost:8000/docs`
- **MLflow UI**: `http://localhost:5000`
- **MLflow API**: `http://localhost:5000/api`

## 🚀 API Endpoints

- `GET /`: Health check
- `POST /predict`: Make predictions
- `GET /models`: List available models
- `GET /experiments`: List MLflow experiments
- `POST /train`: Trigger model training

## 🚀 Next Steps

1. Add more complex ML models
2. Implement model A/B testing
3. Add authentication and authorization
4. Set up automated model deployment
5. Integrate with CI/CD pipeline

## 🐛 Troubleshooting

**MLflow Connection Issues**: Ensure containers are running
```bash
docker-compose ps
```

**FastAPI Issues**: Check the application logs
```bash
uvicorn app.main:app --reload --log-level debug
```

**Model Training Issues**: Check MLflow tracking URI
```bash
mlflow ui --host 0.0.0.0 --port 5000
``` 