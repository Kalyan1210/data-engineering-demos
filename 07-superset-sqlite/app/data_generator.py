import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import os

def generate_sales_data(n_records=1000):
    """Generate sample sales data"""
    np.random.seed(42)
    
    # Date range for the last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate sales records
    sales_data = []
    
    for _ in range(n_records):
        sale_date = np.random.choice(date_range)
        product_id = np.random.randint(1, 21)
        customer_id = np.random.randint(1, 101)
        region_id = np.random.randint(1, 6)
        
        # Generate realistic product prices
        base_price = np.random.uniform(10, 500)
        quantity = np.random.randint(1, 10)
        total_amount = base_price * quantity
        
        sales_data.append({
            'sale_id': _ + 1,
            'sale_date': sale_date.strftime('%Y-%m-%d'),
            'product_id': product_id,
            'customer_id': customer_id,
            'region_id': region_id,
            'quantity': quantity,
            'unit_price': round(base_price, 2),
            'total_amount': round(total_amount, 2)
        })
    
    return pd.DataFrame(sales_data)

def generate_customer_data(n_customers=100):
    """Generate sample customer data"""
    np.random.seed(42)
    
    customer_data = []
    
    for i in range(n_customers):
        customer_data.append({
            'customer_id': i + 1,
            'first_name': f'Customer{i+1}',
            'last_name': f'LastName{i+1}',
            'email': f'customer{i+1}@example.com',
            'age': np.random.randint(18, 80),
            'gender': np.random.choice(['M', 'F']),
            'income_level': np.random.choice(['Low', 'Medium', 'High']),
            'customer_segment': np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum']),
            'registration_date': (datetime.now() - timedelta(days=np.random.randint(1, 1000))).strftime('%Y-%m-%d')
        })
    
    return pd.DataFrame(customer_data)

def generate_product_data(n_products=20):
    """Generate sample product data"""
    np.random.seed(42)
    
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
    brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']
    
    product_data = []
    
    for i in range(n_products):
        product_data.append({
            'product_id': i + 1,
            'product_name': f'Product {i+1}',
            'category': np.random.choice(categories),
            'brand': np.random.choice(brands),
            'price': round(np.random.uniform(10, 500), 2),
            'cost': round(np.random.uniform(5, 250), 2),
            'inventory': np.random.randint(0, 100),
            'supplier_id': np.random.randint(1, 11)
        })
    
    return pd.DataFrame(product_data)

def generate_region_data():
    """Generate sample region data"""
    regions = [
        {'region_id': 1, 'region_name': 'North America', 'country': 'USA', 'population': 331000000},
        {'region_id': 2, 'region_name': 'Europe', 'country': 'Germany', 'population': 83000000},
        {'region_id': 3, 'region_name': 'Asia Pacific', 'country': 'Japan', 'population': 126000000},
        {'region_id': 4, 'region_name': 'Latin America', 'country': 'Brazil', 'population': 212000000},
        {'region_id': 5, 'region_name': 'Middle East', 'country': 'UAE', 'population': 10000000}
    ]
    
    return pd.DataFrame(regions)

def generate_supplier_data(n_suppliers=10):
    """Generate sample supplier data"""
    np.random.seed(42)
    
    supplier_data = []
    
    for i in range(n_suppliers):
        supplier_data.append({
            'supplier_id': i + 1,
            'supplier_name': f'Supplier {i+1}',
            'contact_person': f'Contact {i+1}',
            'email': f'supplier{i+1}@example.com',
            'phone': f'+1-555-{str(i+1).zfill(3)}-{str(i+1).zfill(4)}',
            'address': f'Address {i+1}, City {i+1}',
            'rating': round(np.random.uniform(1, 5), 1)
        })
    
    return pd.DataFrame(supplier_data)

def create_database_schema():
    """Create SQLite database schema"""
    schema = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        age INTEGER,
        gender TEXT,
        income_level TEXT,
        customer_segment TEXT,
        registration_date TEXT
    );

    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        brand TEXT,
        price REAL,
        cost REAL,
        inventory INTEGER,
        supplier_id INTEGER
    );

    CREATE TABLE IF NOT EXISTS regions (
        region_id INTEGER PRIMARY KEY,
        region_name TEXT,
        country TEXT,
        population INTEGER
    );

    CREATE TABLE IF NOT EXISTS suppliers (
        supplier_id INTEGER PRIMARY KEY,
        supplier_name TEXT,
        contact_person TEXT,
        email TEXT,
        phone TEXT,
        address TEXT,
        rating REAL
    );

    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY,
        sale_date TEXT,
        product_id INTEGER,
        customer_id INTEGER,
        region_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        total_amount REAL,
        FOREIGN KEY (product_id) REFERENCES products (product_id),
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
        FOREIGN KEY (region_id) REFERENCES regions (region_id)
    );
    """
    
    return schema

def save_to_sqlite(dataframes, db_path):
    """Save all dataframes to SQLite database"""
    conn = sqlite3.connect(db_path)
    
    # Create schema
    schema = create_database_schema()
    conn.executescript(schema)
    
    # Save each dataframe to its respective table
    for table_name, df in dataframes.items():
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Saved {len(df)} records to {table_name} table")
    
    conn.close()
    print(f"Database created at: {db_path}")

def main():
    """Generate all sample data"""
    print("Generating sample business data...")
    
    # Create data directory if it doesn't exist
    os.makedirs('data/database', exist_ok=True)
    
    # Generate all dataframes
    dataframes = {
        'customers': generate_customer_data(),
        'products': generate_product_data(),
        'regions': generate_region_data(),
        'suppliers': generate_supplier_data(),
        'sales': generate_sales_data()
    }
    
    # Save to SQLite database
    db_path = 'data/database/business.db'
    save_to_sqlite(dataframes, db_path)
    
    # Also save as CSV for reference
    for table_name, df in dataframes.items():
        csv_path = f'data/{table_name}.csv'
        df.to_csv(csv_path, index=False)
        print(f"Saved CSV: {csv_path}")
    
    print("Data generation completed!")

if __name__ == "__main__":
    main() 