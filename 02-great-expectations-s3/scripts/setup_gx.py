#!/usr/bin/env python3
"""
Setup script for Great Expectations with MinIO
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def setup_great_expectations():
    """Initialize Great Expectations project"""
    print("🚀 Setting up Great Expectations...")
    
    # Check if great_expectations is installed
    try:
        import great_expectations
        print("✅ Great Expectations is installed")
    except ImportError:
        print("📦 Installing Great Expectations...")
        run_command("pip install great-expectations")
    
    # Initialize Great Expectations project
    if not os.path.exists("great_expectations"):
        print("📁 Initializing Great Expectations project...")
        run_command("great_expectations init --no-interaction")
    
    # Create data source configuration
    create_data_source_config()
    
    print("✅ Great Expectations setup complete!")

def create_data_source_config():
    """Create data source configuration for MinIO"""
    print("🔧 Configuring MinIO data source...")
    
    # Create great_expectations.yml configuration
    config = {
        "config_version": 3.0,
        "datasources": {
            "minio_datasource": {
                "class_name": "PandasDatasource",
                "data_connectors": {
                    "default_inferred_data_connector_name": {
                        "class_name": "InferredAssetFilesystemDataConnector",
                        "base_directory": "data",
                        "default_regex": {
                            "group_names": ["data_asset_name"],
                            "pattern": "(.*)\\.csv"
                        }
                    }
                }
            }
        },
        "stores": {
            "expectations_store": {
                "class_name": "ExpectationsStore",
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": "expectations/expectations"
                }
            },
            "validations_store": {
                "class_name": "ValidationsStore",
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": "expectations/validations"
                }
            },
            "evaluation_parameter_store": {
                "class_name": "EvaluationParameterStore",
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": "expectations/evaluation_parameters"
                }
            },
            "checkpoint_store": {
                "class_name": "CheckpointStore",
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": "expectations/checkpoints"
                }
            }
        },
        "data_docs_sites": {
            "local_site": {
                "class_name": "SiteBuilder",
                "show_how_to_buttons": True,
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": "expectations/data_docs"
                }
            }
        },
        "validation_operators": {
            "action_list_operator": {
                "class_name": "ActionListValidationOperator",
                "action_list": [
                    {
                        "name": "store_validation_result",
                        "action": {
                            "class_name": "StoreValidationResultAction"
                        }
                    },
                    {
                        "name": "store_evaluation_params",
                        "action": {
                            "class_name": "StoreEvaluationParametersAction"
                        }
                    },
                    {
                        "name": "update_data_docs",
                        "action": {
                            "class_name": "UpdateDataDocsAction"
                        }
                    }
                ]
            }
        }
    }
    
    # Write configuration
    os.makedirs("expectations", exist_ok=True)
    with open("expectations/great_expectations.yml", "w") as f:
        import yaml
        yaml.dump(config, f, default_flow_style=False)
    
    print("✅ Data source configuration created!")

def create_expectation_suite():
    """Create a basic expectation suite"""
    print("📋 Creating expectation suite...")
    
    # Create expectations directory
    os.makedirs("expectations/expectations", exist_ok=True)
    
    # Basic expectation suite
    suite_config = {
        "expectation_suite_name": "employee_data_suite",
        "expectations": [
            {
                "expectation_type": "expect_table_columns_to_match_ordered_list",
                "kwargs": {
                    "column_list": ["id", "name", "email", "age", "salary", "department", "hire_date", "is_active"]
                }
            },
            {
                "expectation_type": "expect_column_values_to_not_be_null",
                "kwargs": {
                    "column": "id"
                }
            },
            {
                "expectation_type": "expect_column_values_to_be_between",
                "kwargs": {
                    "column": "age",
                    "min_value": 18,
                    "max_value": 65
                }
            },
            {
                "expectation_type": "expect_column_values_to_be_between",
                "kwargs": {
                    "column": "salary",
                    "min_value": 30000,
                    "max_value": 200000
                }
            },
            {
                "expectation_type": "expect_column_value_lengths_to_be_between",
                "kwargs": {
                    "column": "email",
                    "min_value": 10,
                    "max_value": 50
                }
            }
        ]
    }
    
    # Write expectation suite
    with open("expectations/expectations/employee_data_suite.json", "w") as f:
        json.dump(suite_config, f, indent=2)
    
    print("✅ Expectation suite created!")

if __name__ == "__main__":
    setup_great_expectations()
    create_expectation_suite()
    print("\n🎉 Setup complete! You can now run the demo.") 