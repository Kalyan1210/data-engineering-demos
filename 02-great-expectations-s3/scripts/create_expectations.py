#!/usr/bin/env python3
"""
Create Great Expectations validation rules
"""

import great_expectations as ge
import pandas as pd
import os

def create_expectation_suite():
    """Create a comprehensive expectation suite for employee data"""
    print("📋 Creating expectation suite for employee data...")
    
    # Load sample data
    df = pd.read_csv('data/clean_data.csv')
    
    # Create expectation suite
    context = ge.get_context()
    suite = context.create_expectation_suite(
        expectation_suite_name="employee_data_suite",
        overwrite_existing=True
    )
    
    # Create batch request
    batch_request = {
        "datasource_name": "minio_datasource",
        "data_connector_name": "default_inferred_data_connector_name",
        "data_asset_name": "clean_data",
        "limit": 1000,
    }
    
    # Get validator
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite=suite
    )
    
    # Add expectations
    print("🔍 Adding data quality expectations...")
    
    # Table-level expectations
    validator.expect_table_columns_to_match_ordered_list(
        column_list=["id", "name", "email", "age", "salary", "department", "hire_date", "is_active"]
    )
    
    validator.expect_table_row_count_to_be_between(min_value=10, max_value=1000)
    
    # Column-level expectations
    # ID column
    validator.expect_column_values_to_not_be_null(column="id")
    validator.expect_column_values_to_be_unique(column="id")
    validator.expect_column_values_to_be_between(column="id", min_value=1, max_value=1000)
    
    # Name column
    validator.expect_column_values_to_not_be_null(column="name")
    validator.expect_column_value_lengths_to_be_between(column="name", min_value=2, max_value=50)
    
    # Email column
    validator.expect_column_values_to_not_be_null(column="email")
    validator.expect_column_value_lengths_to_be_between(column="email", min_value=10, max_value=50)
    validator.expect_column_values_to_match_regex(column="email", regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    
    # Age column
    validator.expect_column_values_to_not_be_null(column="age")
    validator.expect_column_values_to_be_between(column="age", min_value=18, max_value=65)
    
    # Salary column
    validator.expect_column_values_to_not_be_null(column="salary")
    validator.expect_column_values_to_be_between(column="salary", min_value=30000, max_value=200000)
    
    # Department column
    validator.expect_column_values_to_not_be_null(column="department")
    validator.expect_column_values_to_be_in_set(
        column="department", 
        value_set=["Engineering", "Marketing", "Sales", "Finance", "HR"]
    )
    
    # Hire date column
    validator.expect_column_values_to_not_be_null(column="hire_date")
    validator.expect_column_values_to_match_strftime_format(column="hire_date", strftime_format="%Y-%m-%d")
    
    # Is active column
    validator.expect_column_values_to_not_be_null(column="is_active")
    validator.expect_column_values_to_be_in_set(column="is_active", value_set=[True, False])
    
    # Save expectations
    validator.save_expectation_suite()
    print("✅ Expectation suite created and saved!")

def create_custom_expectations():
    """Create custom expectations for specific business rules"""
    print("🔧 Creating custom business rule expectations...")
    
    # Load data
    df = pd.read_csv('data/clean_data.csv')
    
    # Create context and suite
    context = ge.get_context()
    suite = context.create_expectation_suite(
        expectation_suite_name="business_rules_suite",
        overwrite_existing=True
    )
    
    # Create batch request
    batch_request = {
        "datasource_name": "minio_datasource",
        "data_connector_name": "default_inferred_data_connector_name",
        "data_asset_name": "clean_data",
        "limit": 1000,
    }
    
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite=suite
    )
    
    # Business rule: Engineering salaries should be higher than average
    validator.expect_column_mean_to_be_between(
        column="salary",
        min_value=70000,
        max_value=200000,
        condition_parser="pandas",
        row_condition="department == 'Engineering'"
    )
    
    # Business rule: Active employees should have recent hire dates
    validator.expect_column_values_to_be_between(
        column="hire_date",
        min_value="2020-01-01",
        max_value="2024-12-31",
        condition_parser="pandas",
        row_condition="is_active == True"
    )
    
    # Business rule: Email domains should be company.com
    validator.expect_column_values_to_match_regex(
        column="email",
        regex=r".*@company\.com$"
    )
    
    # Save custom expectations
    validator.save_expectation_suite()
    print("✅ Custom business rule expectations created!")

def main():
    """Main function"""
    print("🚀 Creating Great Expectations validation rules...")
    
    # Check if data exists
    if not os.path.exists('data/clean_data.csv'):
        print("❌ Clean data not found. Run generate_data.py first.")
        return
    
    # Create expectation suites
    create_expectation_suite()
    create_custom_expectations()
    
    print("\n🎉 Expectation creation complete!")
    print("📋 Created expectation suites:")
    print("   - employee_data_suite")
    print("   - business_rules_suite")

if __name__ == "__main__":
    main() 