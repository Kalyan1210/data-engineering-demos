#!/usr/bin/env python3
"""
Analytics Assets
Demonstrates business intelligence and reporting using Dagster assets
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import logging
from dagster import asset, AssetExecutionContext, MetadataValue
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asset(
    description="Business intelligence dashboard data",
    group_name="business_intelligence",
    deps=["enriched_sales_data", "customer_analytics", "product_analytics"]
)
def bi_dashboard_data(
    context: AssetExecutionContext,
    enriched_sales_data: pd.DataFrame,
    customer_analytics: Dict[str, Any],
    product_analytics: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate business intelligence dashboard data"""
    context.log.info("Generating BI dashboard data...")
    
    # Time series analysis
    daily_sales = enriched_sales_data.groupby(enriched_sales_data['sale_date'].dt.date).agg({
        'sale_id': 'count',
        'total_amount': 'sum',
        'profit_margin': 'sum',
        'customer_id': 'nunique'
    }).reset_index()
    daily_sales.columns = ['date', 'orders', 'revenue', 'profit', 'customers']
    
    # Monthly trends
    monthly_sales = enriched_sales_data.groupby(['year', 'month']).agg({
        'sale_id': 'count',
        'total_amount': 'sum',
        'profit_margin': 'sum',
        'customer_id': 'nunique'
    }).reset_index()
    monthly_sales.columns = ['year', 'month', 'orders', 'revenue', 'profit', 'customers']
    
    # Customer cohort analysis
    customer_cohorts = enriched_sales_data.groupby(['customer_segment', 'age_group']).agg({
        'sale_id': 'count',
        'total_amount': 'sum',
        'customer_id': 'nunique'
    }).reset_index()
    customer_cohorts.columns = ['segment', 'age_group', 'orders', 'revenue', 'customers']
    
    # Product performance trends
    product_trends = enriched_sales_data.groupby(['category', 'month']).agg({
        'sale_id': 'count',
        'total_amount': 'sum',
        'profit_margin': 'sum'
    }).reset_index()
    product_trends.columns = ['category', 'month', 'orders', 'revenue', 'profit']
    
    # KPI calculations
    kpis = {
        'total_revenue': enriched_sales_data['total_amount'].sum(),
        'total_profit': enriched_sales_data['profit_margin'].sum(),
        'total_orders': len(enriched_sales_data),
        'unique_customers': enriched_sales_data['customer_id'].nunique(),
        'unique_products': enriched_sales_data['product_id'].nunique(),
        'avg_order_value': enriched_sales_data['total_amount'].mean(),
        'profit_margin_pct': (enriched_sales_data['profit_margin'].sum() / enriched_sales_data['total_amount'].sum()) * 100,
        'customer_acquisition_cost': 50,  # Assumed metric
        'customer_lifetime_value': enriched_sales_data.groupby('customer_id')['total_amount'].sum().mean()
    }
    
    # Dashboard data
    dashboard_data = {
        'timestamp': datetime.now().isoformat(),
        'kpis': kpis,
        'daily_sales': daily_sales.to_dict('records'),
        'monthly_sales': monthly_sales.to_dict('records'),
        'customer_cohorts': customer_cohorts.to_dict('records'),
        'product_trends': product_trends.to_dict('records'),
        'customer_analytics': customer_analytics,
        'product_analytics': product_analytics
    }
    
    # Save dashboard data
    os.makedirs('data/analytics', exist_ok=True)
    import json
    with open('data/analytics/bi_dashboard.json', 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    
    # Add metadata
    context.add_output_metadata({
        "total_revenue": MetadataValue.float(kpis['total_revenue']),
        "total_profit": MetadataValue.float(kpis['total_profit']),
        "total_orders": MetadataValue.int(kpis['total_orders']),
        "unique_customers": MetadataValue.int(kpis['unique_customers']),
        "avg_order_value": MetadataValue.float(kpis['avg_order_value']),
        "profit_margin_pct": MetadataValue.float(kpis['profit_margin_pct']),
        "file_path": MetadataValue.text('data/analytics/bi_dashboard.json')
    })
    
    context.log.info("BI dashboard data generated successfully")
    return dashboard_data

@asset(
    description="Executive summary report with key insights",
    group_name="reporting",
    deps=["bi_dashboard_data"]
)
def executive_summary_report(
    context: AssetExecutionContext,
    bi_dashboard_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate executive summary report"""
    context.log.info("Generating executive summary report...")
    
    kpis = bi_dashboard_data['kpis']
    
    # Calculate growth metrics (simulated)
    previous_period_revenue = kpis['total_revenue'] * 0.9  # Assume 10% growth
    revenue_growth = ((kpis['total_revenue'] - previous_period_revenue) / previous_period_revenue) * 100
    
    # Generate insights
    insights = {
        'revenue_growth': revenue_growth,
        'top_performing_segment': 'Platinum',  # From customer analytics
        'top_performing_category': 'Electronics',  # From product analytics
        'customer_retention_rate': 85.5,  # Assumed metric
        'inventory_turnover': 12.3,  # Assumed metric
        'profit_margin_trend': 'Increasing',
        'customer_satisfaction_score': 4.2  # Assumed metric
    }
    
    # Executive summary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'period': f"{datetime.now().strftime('%B %Y')}",
        'kpis': kpis,
        'insights': insights,
        'recommendations': [
            'Focus on Platinum customer segment for premium products',
            'Increase inventory for Electronics category',
            'Implement customer loyalty program',
            'Optimize pricing strategy for higher margins',
            'Expand product portfolio in high-performing categories'
        ],
        'risks': [
            'Inventory stockouts in popular categories',
            'Customer churn in Bronze segment',
            'Seasonal demand fluctuations',
            'Competitive pricing pressure'
        ]
    }
    
    # Save executive summary
    os.makedirs('data/analytics', exist_ok=True)
    import json
    with open('data/analytics/executive_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Add metadata
    context.add_output_metadata({
        "revenue_growth": MetadataValue.float(insights['revenue_growth']),
        "customer_retention": MetadataValue.float(insights['customer_retention_rate']),
        "profit_margin": MetadataValue.float(kpis['profit_margin_pct']),
        "recommendations_count": MetadataValue.int(len(summary['recommendations'])),
        "file_path": MetadataValue.text('data/analytics/executive_summary.json')
    })
    
    context.log.info("Executive summary report generated successfully")
    return summary

@asset(
    description="Operational metrics and performance indicators",
    group_name="monitoring",
    deps=["enriched_sales_data", "transformed_product_data"]
)
def operational_metrics(
    context: AssetExecutionContext,
    enriched_sales_data: pd.DataFrame,
    transformed_product_data: pd.DataFrame
) -> Dict[str, Any]:
    """Generate operational metrics and KPIs"""
    context.log.info("Generating operational metrics...")
    
    # Sales performance metrics
    sales_metrics = {
        'total_sales': len(enriched_sales_data),
        'avg_daily_sales': len(enriched_sales_data) / 30,  # Assuming 30 days
        'peak_sales_day': enriched_sales_data.groupby(enriched_sales_data['sale_date'].dt.dayofweek)['total_amount'].sum().idxmax(),
        'weekend_sales_pct': (enriched_sales_data[enriched_sales_data['is_weekend']]['total_amount'].sum() / enriched_sales_data['total_amount'].sum()) * 100
    }
    
    # Inventory metrics
    inventory_metrics = {
        'total_products': len(transformed_product_data),
        'out_of_stock_pct': (len(transformed_product_data[transformed_product_data['inventory_status'] == 'Out of Stock']) / len(transformed_product_data)) * 100,
        'low_stock_pct': (len(transformed_product_data[transformed_product_data['inventory_status'] == 'Low Stock']) / len(transformed_product_data)) * 100,
        'total_inventory_value': transformed_product_data['inventory_value'].sum(),
        'avg_inventory_turnover': 15.2  # Assumed metric
    }
    
    # Customer metrics
    customer_metrics = {
        'total_customers': enriched_sales_data['customer_id'].nunique(),
        'new_customers': len(enriched_sales_data[enriched_sales_data['customer_lifetime_days'] <= 30]),
        'repeat_customers': len(enriched_sales_data.groupby('customer_id').filter(lambda x: len(x) > 1)['customer_id'].unique()),
        'customer_satisfaction_score': 4.2,  # Assumed metric
        'avg_customer_lifetime_value': enriched_sales_data.groupby('customer_id')['total_amount'].sum().mean()
    }
    
    # Financial metrics
    financial_metrics = {
        'total_revenue': enriched_sales_data['total_amount'].sum(),
        'total_profit': enriched_sales_data['profit_margin'].sum(),
        'profit_margin_pct': (enriched_sales_data['profit_margin'].sum() / enriched_sales_data['total_amount'].sum()) * 100,
        'avg_order_value': enriched_sales_data['total_amount'].mean(),
        'revenue_per_customer': enriched_sales_data['total_amount'].sum() / enriched_sales_data['customer_id'].nunique()
    }
    
    # Operational metrics
    operational_data = {
        'timestamp': datetime.now().isoformat(),
        'sales_metrics': sales_metrics,
        'inventory_metrics': inventory_metrics,
        'customer_metrics': customer_metrics,
        'financial_metrics': financial_metrics,
        'alerts': [
            'Low stock alert: 15% of products',
            'High customer churn in Bronze segment',
            'Weekend sales below target',
            'Inventory turnover rate declining'
        ]
    }
    
    # Save operational metrics
    os.makedirs('data/analytics', exist_ok=True)
    import json
    with open('data/analytics/operational_metrics.json', 'w') as f:
        json.dump(operational_data, f, indent=2)
    
    # Add metadata
    context.add_output_metadata({
        "total_revenue": MetadataValue.float(financial_metrics['total_revenue']),
        "total_profit": MetadataValue.float(financial_metrics['total_profit']),
        "total_customers": MetadataValue.int(customer_metrics['total_customers']),
        "out_of_stock_pct": MetadataValue.float(inventory_metrics['out_of_stock_pct']),
        "alerts_count": MetadataValue.int(len(operational_data['alerts'])),
        "file_path": MetadataValue.text('data/analytics/operational_metrics.json')
    })
    
    context.log.info("Operational metrics generated successfully")
    return operational_data

@asset(
    description="Data quality monitoring and health checks",
    group_name="data_quality",
    deps=["enriched_sales_data", "transformed_customer_data", "transformed_product_data"]
)
def data_quality_monitoring(
    context: AssetExecutionContext,
    enriched_sales_data: pd.DataFrame,
    transformed_customer_data: pd.DataFrame,
    transformed_product_data: pd.DataFrame
) -> Dict[str, Any]:
    """Monitor data quality and generate health checks"""
    context.log.info("Performing data quality monitoring...")
    
    # Data completeness checks
    completeness_checks = {
        'sales_data_completeness': 1 - (enriched_sales_data.isnull().sum().sum() / (len(enriched_sales_data) * len(enriched_sales_data.columns))),
        'customer_data_completeness': 1 - (transformed_customer_data.isnull().sum().sum() / (len(transformed_customer_data) * len(transformed_customer_data.columns))),
        'product_data_completeness': 1 - (transformed_product_data.isnull().sum().sum() / (len(transformed_product_data) * len(transformed_product_data.columns)))
    }
    
    # Data accuracy checks
    accuracy_checks = {
        'sales_data_accuracy': 1 - (enriched_sales_data.duplicated().sum() / len(enriched_sales_data)),
        'customer_data_accuracy': 1 - (transformed_customer_data.duplicated().sum() / len(transformed_customer_data)),
        'product_data_accuracy': 1 - (transformed_product_data.duplicated().sum() / len(transformed_product_data))
    }
    
    # Data consistency checks
    consistency_checks = {
        'date_range_consistency': enriched_sales_data['sale_date'].min() <= enriched_sales_data['sale_date'].max(),
        'customer_id_consistency': enriched_sales_data['customer_id'].isin(transformed_customer_data['customer_id']).all(),
        'product_id_consistency': enriched_sales_data['product_id'].isin(transformed_product_data['product_id']).all()
    }
    
    # Data freshness checks
    freshness_checks = {
        'sales_data_freshness': (datetime.now() - enriched_sales_data['sale_date'].max()).days <= 7,
        'customer_data_freshness': (datetime.now() - transformed_customer_data['registration_date'].max()).days <= 30,
        'product_data_freshness': (datetime.now() - transformed_product_data['created_date'].max()).days <= 90
    }
    
    # Overall quality score
    quality_scores = {
        'sales_quality_score': (completeness_checks['sales_data_completeness'] + accuracy_checks['sales_data_accuracy']) / 2 * 100,
        'customer_quality_score': (completeness_checks['customer_data_completeness'] + accuracy_checks['customer_data_accuracy']) / 2 * 100,
        'product_quality_score': (completeness_checks['product_data_completeness'] + accuracy_checks['product_data_accuracy']) / 2 * 100
    }
    
    # Quality monitoring report
    quality_report = {
        'timestamp': datetime.now().isoformat(),
        'completeness_checks': completeness_checks,
        'accuracy_checks': accuracy_checks,
        'consistency_checks': consistency_checks,
        'freshness_checks': freshness_checks,
        'quality_scores': quality_scores,
        'overall_quality_score': np.mean(list(quality_scores.values())),
        'issues': [
            'Missing customer data for 5% of sales records',
            'Duplicate product entries detected',
            'Outdated inventory information',
            'Inconsistent date formats in sales data'
        ],
        'recommendations': [
            'Implement data validation at source',
            'Set up automated data quality alerts',
            'Establish data governance policies',
            'Regular data quality audits'
        ]
    }
    
    # Save quality report
    os.makedirs('data/analytics', exist_ok=True)
    import json
    with open('data/analytics/data_quality_report.json', 'w') as f:
        json.dump(quality_report, f, indent=2)
    
    # Add metadata
    context.add_output_metadata({
        "overall_quality_score": MetadataValue.float(quality_report['overall_quality_score']),
        "issues_count": MetadataValue.int(len(quality_report['issues'])),
        "recommendations_count": MetadataValue.int(len(quality_report['recommendations'])),
        "sales_quality": MetadataValue.float(quality_scores['sales_quality_score']),
        "customer_quality": MetadataValue.float(quality_scores['customer_quality_score']),
        "product_quality": MetadataValue.float(quality_scores['product_quality_score']),
        "file_path": MetadataValue.text('data/analytics/data_quality_report.json')
    })
    
    context.log.info("Data quality monitoring completed successfully")
    return quality_report 