from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import os
import requests

from . import models
from . import schemas

# Initialize FastAPI app
app = FastAPI(
    title="ML Model API",
    description="A FastAPI application for ML model serving with MLflow tracking",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MLflow configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "ML Model API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Health check for Docker"""
    return {"status": "healthy"}

@app.post("/predict", response_model=schemas.PredictionResponse)
async def predict(request: schemas.PredictionRequest):
    """Make predictions using the latest model"""
    try:
        # Load the latest model from MLflow
        model = models.load_latest_model()
        
        # Prepare input data
        input_data = np.array(request.features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0].tolist() if hasattr(model, 'predict_proba') else None
        
        return schemas.PredictionResponse(
            prediction=float(prediction),
            probabilities=probability,
            model_version=model.__class__.__name__
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/models")
async def list_models():
    """List available models in MLflow"""
    try:
        client = mlflow.tracking.MlflowClient()
        registered_models = client.list_registered_models()
        
        models_info = []
        for model in registered_models:
            latest_version = client.get_latest_versions(model.name, stages=["None"])
            if latest_version:
                models_info.append({
                    "name": model.name,
                    "version": latest_version[0].version,
                    "stage": latest_version[0].current_stage,
                    "description": model.description
                })
        
        return {"models": models_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list models: {str(e)}")

@app.get("/experiments")
async def list_experiments():
    """List MLflow experiments"""
    try:
        client = mlflow.tracking.MlflowClient()
        experiments = client.list_experiments()
        
        experiments_info = []
        for exp in experiments:
            experiments_info.append({
                "experiment_id": exp.experiment_id,
                "name": exp.name,
                "lifecycle_stage": exp.lifecycle_stage
            })
        
        return {"experiments": experiments_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list experiments: {str(e)}")

@app.post("/train")
async def train_model(request: schemas.TrainingRequest):
    """Trigger model training"""
    try:
        # Import here to avoid circular imports
        from ..scripts.train_model import train_and_log_model
        
        # Train model with MLflow tracking
        experiment_name = request.experiment_name or "default"
        model_name = request.model_name or "iris_classifier"
        
        # Run training
        run_id = train_and_log_model(
            experiment_name=experiment_name,
            model_name=model_name,
            random_state=request.random_state or 42
        )
        
        return {
            "message": "Model training completed successfully",
            "run_id": run_id,
            "experiment_name": experiment_name,
            "model_name": model_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.get("/metrics/{run_id}")
async def get_metrics(run_id: str):
    """Get metrics for a specific MLflow run"""
    try:
        client = mlflow.tracking.MlflowClient()
        run = client.get_run(run_id)
        
        return {
            "run_id": run_id,
            "metrics": run.data.metrics,
            "params": run.data.params,
            "tags": run.data.tags
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 