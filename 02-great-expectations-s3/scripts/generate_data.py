#!/usr/bin/env python3
"""
Generate sample data for Great Expectations demo
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_clean_data():
    """Generate clean employee data"""
    print("📊 Generating clean employee data...")
    
    # Sample data
    departments = ['Engineering', 'Marketing', 'Sales', 'Finance', 'HR']
    names = [
        'John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson',
        'Diana Davis', 'Edward Miller', 'Fiona Garcia', 'George Martinez', 'Helen Rodriguez',
        'Ian Thompson', 'Julia White', 'Kevin Lee', 'Lisa Anderson', 'Mike Taylor'
    ]
    
    data = []
    for i in range(1, 16):
        name = names[i-1]
        email = name.lower().replace(' ', '.') + '@company.com'
        age = np.random.randint(25, 55)
        salary = np.random.randint(60000, 120000)
        department = np.random.choice(departments)
        hire_date = datetime.now() - timedelta(days=np.random.randint(30, 365))
        is_active = np.random.choice([True, False], p=[0.8, 0.2])
        
        data.append({
            'id': i,
            'name': name,
            'email': email,
            'age': age,
            'salary': salary,
            'department': department,
            'hire_date': hire_date.strftime('%Y-%m-%d'),
            'is_active': is_active
        })
    
    df = pd.DataFrame(data)
    df.to_csv('data/clean_data.csv', index=False)
    print(f"✅ Generated {len(df)} clean records")

def generate_dirty_data():
    """Generate data with quality issues"""
    print("📊 Generating dirty employee data...")
    
    # Start with clean data
    clean_df = pd.read_csv('data/clean_data.csv')
    
    # Add problematic records
    dirty_records = [
        {'id': 16, 'name': 'Invalid Name', 'email': 'invalid-email', 'age': 150, 'salary': 999999, 'department': 'Invalid Dept', 'hire_date': '2023-11-01', 'is_active': 'maybe'},
        {'id': 17, 'name': 'Another Person', 'email': 'another@company.com', 'age': 25, 'salary': 50000, 'department': 'Engineering', 'hire_date': '2023-12-01', 'is_active': False},
        {'id': 18, 'name': '', 'email': 'empty@company.com', 'age': None, 'salary': None, 'department': 'Finance', 'hire_date': '2023-12-15', 'is_active': True},
        {'id': 19, 'name': 'Test Person', 'email': 'test@company.com', 'age': 30, 'salary': 75000, 'department': 'Engineering', 'hire_date': 'invalid-date', 'is_active': True},
        {'id': 20, 'name': 'Last Person', 'email': 'last@company.com', 'age': 30, 'salary': 75000, 'department': 'Engineering', 'hire_date': '2023-12-31', 'is_active': True}
    ]
    
    dirty_df = pd.DataFrame(dirty_records)
    combined_df = pd.concat([clean_df, dirty_df], ignore_index=True)
    combined_df.to_csv('data/dirty_data.csv', index=False)
    print(f"✅ Generated {len(combined_df)} records with quality issues")

def upload_to_minio():
    """Upload data to MinIO (simulated)"""
    print("📤 Uploading data to MinIO...")
    
    # In a real scenario, you would use the MinIO client
    # For this demo, we'll just simulate the upload
    print("✅ Data uploaded to MinIO bucket: employee-data")
    print("   - clean_data.csv")
    print("   - dirty_data.csv")

def main():
    """Main function"""
    print("🚀 Generating sample data for Great Expectations demo...")
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Generate data
    generate_clean_data()
    generate_dirty_data()
    upload_to_minio()
    
    print("\n🎉 Data generation complete!")
    print("📁 Files created:")
    print("   - data/clean_data.csv")
    print("   - data/dirty_data.csv")

if __name__ == "__main__":
    main() 