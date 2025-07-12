#!/usr/bin/env python3
"""
Generate sample data for the FastAPI + MLflow demo
"""

import pandas as pd
import numpy as np
from sklearn.datasets import load_iris, make_classification
import os

def generate_iris_data():
    """Generate iris dataset for training"""
    print("🌺 Generating iris dataset...")
    
    # Load iris dataset
    iris = load_iris()
    
    # Create DataFrame
    feature_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    df = pd.DataFrame(iris.data, columns=feature_names)
    df['target'] = iris.target
    df['target_name'] = [iris.target_names[i] for i in iris.target]
    
    # Split into train and test
    train_size = int(0.8 * len(df))
    train_df = df[:train_size]
    test_df = df[train_size:]
    
    # Save datasets
    os.makedirs('data', exist_ok=True)
    train_df.to_csv('data/train.csv', index=False)
    test_df.to_csv('data/test.csv', index=False)
    
    print(f"✅ Generated {len(train_df)} training samples and {len(test_df)} test samples")
    print("📁 Files created:")
    print("   - data/train.csv")
    print("   - data/test.csv")

def generate_synthetic_data():
    """Generate synthetic classification data"""
    print("🔧 Generating synthetic classification data...")
    
    # Generate synthetic data
    X, y = make_classification(
        n_samples=1000,
        n_features=10,
        n_informative=8,
        n_redundant=2,
        n_classes=3,
        random_state=42
    )
    
    # Create DataFrame
    feature_names = [f'feature_{i}' for i in range(X.shape[1])]
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    
    # Split into train and test
    train_size = int(0.8 * len(df))
    train_df = df[:train_size]
    test_df = df[train_size:]
    
    # Save datasets
    train_df.to_csv('data/synthetic_train.csv', index=False)
    test_df.to_csv('data/synthetic_test.csv', index=False)
    
    print(f"✅ Generated {len(train_df)} training samples and {len(test_df)} test samples")
    print("📁 Files created:")
    print("   - data/synthetic_train.csv")
    print("   - data/synthetic_test.csv")

def generate_regression_data():
    """Generate synthetic regression data"""
    print("📈 Generating synthetic regression data...")
    
    # Generate synthetic regression data
    np.random.seed(42)
    n_samples = 1000
    n_features = 5
    
    # Generate features
    X = np.random.randn(n_samples, n_features)
    
    # Generate target with some noise
    coefficients = np.random.randn(n_features)
    y = X @ coefficients + np.random.randn(n_samples) * 0.1
    
    # Create DataFrame
    feature_names = [f'feature_{i}' for i in range(n_features)]
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    
    # Split into train and test
    train_size = int(0.8 * len(df))
    train_df = df[:train_size]
    test_df = df[train_size:]
    
    # Save datasets
    train_df.to_csv('data/regression_train.csv', index=False)
    test_df.to_csv('data/regression_test.csv', index=False)
    
    print(f"✅ Generated {len(train_df)} training samples and {len(test_df)} test samples")
    print("📁 Files created:")
    print("   - data/regression_train.csv")
    print("   - data/regression_test.csv")

def create_sample_predictions():
    """Create sample prediction data"""
    print("🎯 Creating sample prediction data...")
    
    # Sample iris predictions
    sample_features = [
        [5.1, 3.5, 1.4, 0.2],  # Setosa
        [6.3, 3.3, 4.7, 1.6],  # Versicolor
        [6.5, 3.0, 5.2, 2.0],  # Virginica
        [5.0, 3.6, 1.4, 0.2],  # Setosa
        [6.7, 3.0, 5.0, 1.7]   # Virginica
    ]
    
    sample_data = pd.DataFrame(
        sample_features,
        columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    )
    
    sample_data.to_csv('data/sample_predictions.csv', index=False)
    
    print("✅ Created sample prediction data")
    print("📁 File created: data/sample_predictions.csv")

def main():
    """Main function"""
    print("🚀 Generating sample data for FastAPI + MLflow demo...")
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Generate different types of data
    generate_iris_data()
    generate_synthetic_data()
    generate_regression_data()
    create_sample_predictions()
    
    print("\n🎉 Data generation complete!")
    print("📊 Available datasets:")
    print("   - Iris classification (train.csv, test.csv)")
    print("   - Synthetic classification (synthetic_train.csv, synthetic_test.csv)")
    print("   - Regression (regression_train.csv, regression_test.csv)")
    print("   - Sample predictions (sample_predictions.csv)")

if __name__ == "__main__":
    main() 