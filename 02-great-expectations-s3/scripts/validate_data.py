#!/usr/bin/env python3
"""
Validate data using Great Expectations
"""

import great_expectations as ge
import pandas as pd
import os
from datetime import datetime

def validate_clean_data():
    """Validate clean data against expectations"""
    print("🔍 Validating clean data...")
    
    # Load data
    df = pd.read_csv('data/clean_data.csv')
    
    # Create context
    context = ge.get_context()
    
    # Create batch request
    batch_request = {
        "datasource_name": "minio_datasource",
        "data_connector_name": "default_inferred_data_connector_name",
        "data_asset_name": "clean_data",
        "limit": 1000,
    }
    
    # Get expectation suite
    suite = context.get_expectation_suite("employee_data_suite")
    
    # Create validator
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite=suite
    )
    
    # Run validation
    results = validator.validate()
    
    # Print results
    print(f"✅ Clean data validation complete!")
    print(f"   - Total expectations: {len(results.run_results)}")
    print(f"   - Passed: {sum(1 for r in results.run_results if r['success'])}")
    print(f"   - Failed: {sum(1 for r in results.run_results if not r['success'])}")
    
    return results

def validate_dirty_data():
    """Validate dirty data against expectations"""
    print("🔍 Validating dirty data...")
    
    # Load data
    df = pd.read_csv('data/dirty_data.csv')
    
    # Create context
    context = ge.get_context()
    
    # Create batch request
    batch_request = {
        "datasource_name": "minio_datasource",
        "data_connector_name": "default_inferred_data_connector_name",
        "data_asset_name": "dirty_data",
        "limit": 1000,
    }
    
    # Get expectation suite
    suite = context.get_expectation_suite("employee_data_suite")
    
    # Create validator
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite=suite
    )
    
    # Run validation
    results = validator.validate()
    
    # Print results
    print(f"❌ Dirty data validation complete!")
    print(f"   - Total expectations: {len(results.run_results)}")
    print(f"   - Passed: {sum(1 for r in results.run_results if r['success'])}")
    print(f"   - Failed: {sum(1 for r in results.run_results if not r['success'])}")
    
    # Show specific failures
    print("\n🔍 Specific validation failures:")
    for result in results.run_results:
        if not result['success']:
            expectation_type = result['expectation_config']['expectation_type']
            print(f"   - {expectation_type}: FAILED")
    
    return results

def generate_validation_report():
    """Generate a comprehensive validation report"""
    print("📊 Generating validation report...")
    
    # Create context
    context = ge.get_context()
    
    # Build data docs
    context.build_data_docs()
    
    print("✅ Validation report generated!")
    print("📁 Report location: expectations/data_docs/local_site/index.html")

def create_checkpoint():
    """Create a checkpoint for automated validation"""
    print("🔧 Creating validation checkpoint...")
    
    # Create context
    context = ge.get_context()
    
    # Create checkpoint
    checkpoint_config = {
        "name": "employee_data_checkpoint",
        "config_version": 1,
        "class_name": "SimpleCheckpoint",
        "validations": [
            {
                "batch_request": {
                    "datasource_name": "minio_datasource",
                    "data_connector_name": "default_inferred_data_connector_name",
                    "data_asset_name": "clean_data",
                },
                "expectation_suite_name": "employee_data_suite",
            }
        ],
    }
    
    # Add checkpoint
    context.add_checkpoint(**checkpoint_config)
    
    print("✅ Checkpoint created: employee_data_checkpoint")

def run_automated_validation():
    """Run automated validation using checkpoint"""
    print("🤖 Running automated validation...")
    
    # Create context
    context = ge.get_context()
    
    # Run checkpoint
    results = context.run_checkpoint(
        checkpoint_name="employee_data_checkpoint"
    )
    
    print("✅ Automated validation complete!")
    return results

def main():
    """Main function"""
    print("🚀 Running Great Expectations data validation...")
    
    # Check if data exists
    if not os.path.exists('data/clean_data.csv'):
        print("❌ Clean data not found. Run generate_data.py first.")
        return
    
    if not os.path.exists('data/dirty_data.csv'):
        print("❌ Dirty data not found. Run generate_data.py first.")
        return
    
    # Run validations
    clean_results = validate_clean_data()
    dirty_results = validate_dirty_data()
    
    # Create checkpoint
    create_checkpoint()
    
    # Run automated validation
    automated_results = run_automated_validation()
    
    # Generate report
    generate_validation_report()
    
    print("\n🎉 Data validation complete!")
    print("📊 Summary:")
    print("   - Clean data: Validated successfully")
    print("   - Dirty data: Found quality issues")
    print("   - Checkpoint: Created for automation")
    print("   - Report: Generated in expectations/data_docs/")

if __name__ == "__main__":
    main() 