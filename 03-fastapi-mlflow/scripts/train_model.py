#!/usr/bin/env python3
"""
Train and log models with MLflow tracking
"""

import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.datasets import load_iris
import os
import sys

# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import evaluate_model, log_model_metrics

# MLflow configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

def train_and_log_model(
    experiment_name: str = "iris_experiment",
    model_name: str = "iris_classifier",
    random_state: int = 42
) -> str:
    """Train a model and log it to MLflow"""
    
    print(f"🚀 Training model with experiment: {experiment_name}")
    
    # Set the experiment
    mlflow.set_experiment(experiment_name)
    
    # Load data
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )
    
    # Start MLflow run
    with mlflow.start_run() as run:
        print(f"📊 MLflow run ID: {run.info.run_id}")
        
        # Log parameters
        params = {
            "n_estimators": 100,
            "max_depth": 10,
            "random_state": random_state,
            "test_size": 0.2
        }
        
        for param_name, param_value in params.items():
            mlflow.log_param(param_name, param_value)
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=params["n_estimators"],
            max_depth=params["max_depth"],
            random_state=params["random_state"]
        )
        
        print("🔧 Training Random Forest model...")
        model.fit(X_train, y_train)
        
        # Evaluate model
        print("📈 Evaluating model performance...")
        metrics = evaluate_model(model, X_test, y_test)
        
        # Log metrics
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)
            print(f"   {metric_name}: {metric_value:.4f}")
        
        # Log model
        mlflow.sklearn.log_model(
            model,
            "model",
            registered_model_name=model_name
        )
        
        # Log feature names
        feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        mlflow.log_param("feature_names", feature_names)
        
        # Log confusion matrix
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        mlflow.log_artifact("confusion_matrix.txt", str(cm))
        
        print("✅ Model training and logging completed!")
        print(f"📊 Model registered as: {model_name}")
        
        return run.info.run_id

def train_with_hyperparameter_tuning(
    experiment_name: str = "iris_hyperparameter_tuning",
    model_name: str = "iris_classifier_tuned"
) -> str:
    """Train model with hyperparameter tuning"""
    
    print(f"🔍 Training model with hyperparameter tuning...")
    
    # Set the experiment
    mlflow.set_experiment(experiment_name)
    
    # Load data
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Define parameter grid
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [5, 10, 15, None],
        'min_samples_split': [2, 5, 10]
    }
    
    # Start MLflow run
    with mlflow.start_run() as run:
        print(f"📊 MLflow run ID: {run.info.run_id}")
        
        # Grid search
        grid_search = GridSearchCV(
            RandomForestClassifier(random_state=42),
            param_grid,
            cv=5,
            scoring='accuracy',
            n_jobs=-1
        )
        
        print("🔧 Performing grid search...")
        grid_search.fit(X_train, y_train)
        
        # Get best model
        best_model = grid_search.best_estimator_
        
        # Log best parameters
        for param_name, param_value in grid_search.best_params_.items():
            mlflow.log_param(f"best_{param_name}", param_value)
        
        # Log all parameters
        for param_name, param_value in grid_search.best_params_.items():
            mlflow.log_param(param_name, param_value)
        
        # Evaluate best model
        metrics = evaluate_model(best_model, X_test, y_test)
        
        # Log metrics
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)
            print(f"   {metric_name}: {metric_value:.4f}")
        
        # Log model
        mlflow.sklearn.log_model(
            best_model,
            "model",
            registered_model_name=model_name
        )
        
        print("✅ Hyperparameter tuning completed!")
        print(f"📊 Best model registered as: {model_name}")
        
        return run.info.run_id

def compare_models():
    """Compare different model types"""
    
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier
    
    models = {
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "LogisticRegression": LogisticRegression(random_state=42),
        "SVM": SVC(probability=True, random_state=42),
        "DecisionTree": DecisionTreeClassifier(random_state=42)
    }
    
    # Load data
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    results = {}
    
    for model_name, model in models.items():
        print(f"🔧 Training {model_name}...")
        
        # Set experiment
        mlflow.set_experiment(f"model_comparison_{model_name}")
        
        with mlflow.start_run() as run:
            # Train model
            model.fit(X_train, y_train)
            
            # Evaluate
            metrics = evaluate_model(model, X_test, y_test)
            
            # Log metrics
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)
            
            # Log model
            mlflow.sklearn.log_model(
                model,
                "model",
                registered_model_name=f"iris_{model_name.lower()}"
            )
            
            results[model_name] = metrics
            print(f"   Accuracy: {metrics['accuracy']:.4f}")
    
    return results

def main():
    """Main function"""
    print("🚀 Starting model training with MLflow tracking...")
    
    # Train basic model
    run_id = train_and_log_model()
    print(f"✅ Basic model training completed. Run ID: {run_id}")
    
    # Train with hyperparameter tuning
    tuned_run_id = train_with_hyperparameter_tuning()
    print(f"✅ Hyperparameter tuning completed. Run ID: {tuned_run_id}")
    
    # Compare models
    print("\n🔍 Comparing different model types...")
    results = compare_models()
    
    print("\n📊 Model Comparison Results:")
    for model_name, metrics in results.items():
        print(f"   {model_name}: {metrics['accuracy']:.4f}")
    
    print("\n🎉 All model training completed!")
    print("📊 View results in MLflow UI: http://localhost:5000")

if __name__ == "__main__":
    main() 