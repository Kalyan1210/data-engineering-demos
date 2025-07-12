from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class PredictionRequest(BaseModel):
    """Request schema for model predictions"""
    features: List[float] = Field(..., description="Input features for prediction")
    
    class Config:
        schema_extra = {
            "example": {
                "features": [5.1, 3.5, 1.4, 0.2]
            }
        }

class PredictionResponse(BaseModel):
    """Response schema for model predictions"""
    prediction: float = Field(..., description="Model prediction")
    probabilities: Optional[List[float]] = Field(None, description="Prediction probabilities")
    model_version: str = Field(..., description="Model version used for prediction")
    
    class Config:
        schema_extra = {
            "example": {
                "prediction": 0.0,
                "probabilities": [0.9, 0.05, 0.05],
                "model_version": "RandomForestClassifier"
            }
        }

class TrainingRequest(BaseModel):
    """Request schema for model training"""
    experiment_name: Optional[str] = Field("default", description="MLflow experiment name")
    model_name: Optional[str] = Field("iris_classifier", description="Model name for registration")
    random_state: Optional[int] = Field(42, description="Random state for reproducibility")
    
    class Config:
        schema_extra = {
            "example": {
                "experiment_name": "iris_experiment",
                "model_name": "iris_classifier",
                "random_state": 42
            }
        }

class ModelInfo(BaseModel):
    """Schema for model information"""
    name: str = Field(..., description="Model name")
    version: str = Field(..., description="Model version")
    stage: str = Field(..., description="Model stage")
    description: Optional[str] = Field(None, description="Model description")

class ExperimentInfo(BaseModel):
    """Schema for experiment information"""
    experiment_id: str = Field(..., description="Experiment ID")
    name: str = Field(..., description="Experiment name")
    lifecycle_stage: str = Field(..., description="Experiment lifecycle stage")

class MetricsResponse(BaseModel):
    """Schema for MLflow metrics response"""
    run_id: str = Field(..., description="MLflow run ID")
    metrics: Dict[str, float] = Field(..., description="Model metrics")
    params: Dict[str, str] = Field(..., description="Model parameters")
    tags: Dict[str, str] = Field(..., description="Run tags")

class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str = Field(..., description="Service status")
    message: Optional[str] = Field(None, description="Additional message")

class TrainingResponse(BaseModel):
    """Schema for training response"""
    message: str = Field(..., description="Training status message")
    run_id: str = Field(..., description="MLflow run ID")
    experiment_name: str = Field(..., description="Experiment name")
    model_name: str = Field(..., description="Model name") 