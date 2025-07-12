import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from typing import Tuple, Any

# MLflow configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

def load_latest_model():
    """Load the latest model from MLflow"""
    try:
        # Try to load the latest model from MLflow
        client = mlflow.tracking.MlflowClient()
        model_name = "iris_classifier"
        
        # Get the latest version
        latest_version = client.get_latest_versions(model_name, stages=["None"])
        if latest_version:
            model_uri = f"models:/{model_name}/latest"
            model = mlflow.sklearn.load_model(model_uri)
            return model
        else:
            # If no model is registered, train a new one
            print("No registered model found. Training a new model...")
            return train_default_model()
    except Exception as e:
        print(f"Error loading model: {e}")
        # Fallback to training a new model
        return train_default_model()

def train_default_model():
    """Train a default model if no model is available"""
    from sklearn.datasets import load_iris
    
    # Load iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Log to MLflow
    with mlflow.start_run():
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("random_state", 42)
        
        # Make predictions
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "iris_classifier")
    
    return model

def prepare_iris_data() -> Tuple[np.ndarray, np.ndarray]:
    """Prepare iris dataset for training"""
    from sklearn.datasets import load_iris
    
    iris = load_iris()
    return iris.data, iris.target

def evaluate_model(model: Any, X_test: np.ndarray, y_test: np.ndarray) -> dict:
    """Evaluate model performance"""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Generate classification report
    report = classification_report(y_test, y_pred, output_dict=True)
    
    return {
        "accuracy": accuracy,
        "precision": report["weighted avg"]["precision"],
        "recall": report["weighted avg"]["recall"],
        "f1_score": report["weighted avg"]["f1-score"]
    }

def log_model_metrics(model: Any, X_test: np.ndarray, y_test: np.ndarray):
    """Log model metrics to MLflow"""
    metrics = evaluate_model(model, X_test, y_test)
    
    for metric_name, metric_value in metrics.items():
        mlflow.log_metric(metric_name, metric_value)
    
    return metrics

def save_model_locally(model: Any, model_path: str = "models/model.pkl"):
    """Save model locally as backup"""
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model saved locally at: {model_path}")

def load_model_locally(model_path: str = "models/model.pkl"):
    """Load model from local storage"""
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        print(f"Local model not found at: {model_path}")
        return None 