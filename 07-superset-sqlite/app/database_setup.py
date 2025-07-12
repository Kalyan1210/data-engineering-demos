import sqlite3
import os
import pandas as pd
from typing import Dict, List, Any

class SQLiteManager:
    """SQLite database manager for Superset integration"""
    
    def __init__(self, db_path: str = "data/database/business.db"):
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            self.connection = sqlite3.connect(self.db_path)
            print(f"Connected to SQLite database: {self.db_path}")
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("Database connection closed")
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results"""
        if not self.connection:
            print("No database connection")
            return []
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            
            # Get column names
            columns = [description[0] for description in cursor.description]
            
            # Fetch results
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            return []
    
    def get_table_info(self) -> List[Dict[str, Any]]:
        """Get information about all tables"""
        query = """
        SELECT name, sql FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """
        return self.execute_query(query)
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get schema for a specific table"""
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)
    
    def get_table_count(self, table_name: str) -> int:
        """Get row count for a table"""
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0
    
    def get_sample_data(self, table_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get sample data from a table"""
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return self.execute_query(query)
    
    def run_analytics_queries(self) -> Dict[str, Any]:
        """Run common analytics queries"""
        analytics = {}
        
        # Total sales
        query = "SELECT SUM(total_amount) as total_sales FROM sales"
        result = self.execute_query(query)
        analytics['total_sales'] = result[0]['total_sales'] if result else 0
        
        # Sales by region
        query = """
        SELECT r.region_name, SUM(s.total_amount) as region_sales
        FROM sales s
        JOIN regions r ON s.region_id = r.region_id
        GROUP BY r.region_name
        ORDER BY region_sales DESC
        """
        analytics['sales_by_region'] = self.execute_query(query)
        
        # Top products
        query = """
        SELECT p.product_name, SUM(s.total_amount) as product_sales
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY product_sales DESC
        LIMIT 10
        """
        analytics['top_products'] = self.execute_query(query)
        
        # Customer segments
        query = """
        SELECT c.customer_segment, COUNT(*) as customer_count
        FROM customers c
        GROUP BY c.customer_segment
        ORDER BY customer_count DESC
        """
        analytics['customer_segments'] = self.execute_query(query)
        
        # Monthly sales trend
        query = """
        SELECT 
            strftime('%Y-%m', sale_date) as month,
            SUM(total_amount) as monthly_sales
        FROM sales
        GROUP BY month
        ORDER BY month
        """
        analytics['monthly_sales'] = self.execute_query(query)
        
        return analytics
    
    def create_views(self):
        """Create useful views for Superset"""
        views = {
            'sales_summary': """
                CREATE VIEW IF NOT EXISTS sales_summary AS
                SELECT 
                    s.sale_date,
                    p.product_name,
                    p.category,
                    c.customer_segment,
                    r.region_name,
                    s.quantity,
                    s.total_amount
                FROM sales s
                JOIN products p ON s.product_id = p.product_id
                JOIN customers c ON s.customer_id = c.customer_id
                JOIN regions r ON s.region_id = r.region_id
            """,
            
            'customer_analytics': """
                CREATE VIEW IF NOT EXISTS customer_analytics AS
                SELECT 
                    c.customer_id,
                    c.first_name,
                    c.last_name,
                    c.customer_segment,
                    c.income_level,
                    COUNT(s.sale_id) as total_purchases,
                    SUM(s.total_amount) as total_spent,
                    AVG(s.total_amount) as avg_purchase
                FROM customers c
                LEFT JOIN sales s ON c.customer_id = s.customer_id
                GROUP BY c.customer_id
            """,
            
            'product_performance': """
                CREATE VIEW IF NOT EXISTS product_performance AS
                SELECT 
                    p.product_id,
                    p.product_name,
                    p.category,
                    p.brand,
                    p.price,
                    p.inventory,
                    COUNT(s.sale_id) as units_sold,
                    SUM(s.total_amount) as revenue,
                    AVG(s.unit_price) as avg_selling_price
                FROM products p
                LEFT JOIN sales s ON p.product_id = s.product_id
                GROUP BY p.product_id
            """
        }
        
        for view_name, view_sql in views.items():
            try:
                self.connection.executescript(view_sql)
                print(f"Created view: {view_name}")
            except Exception as e:
                print(f"Error creating view {view_name}: {e}")
    
    def export_to_csv(self, output_dir: str = "data"):
        """Export all tables to CSV files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Get all table names
        tables = self.get_table_info()
        
        for table in tables:
            table_name = table['name']
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, self.connection)
            
            csv_path = os.path.join(output_dir, f"{table_name}.csv")
            df.to_csv(csv_path, index=False)
            print(f"Exported {table_name} to {csv_path}")

def main():
    """Test database operations"""
    db_manager = SQLiteManager()
    
    if db_manager.connect():
        # Get table information
        tables = db_manager.get_table_info()
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table['name']}")
        
        # Run analytics
        analytics = db_manager.run_analytics_queries()
        print(f"\nAnalytics Results:")
        print(f"  Total Sales: ${analytics['total_sales']:,.2f}")
        print(f"  Top Products: {len(analytics['top_products'])} products")
        print(f"  Customer Segments: {len(analytics['customer_segments'])} segments")
        
        # Create views
        db_manager.create_views()
        
        # Export to CSV
        db_manager.export_to_csv()
        
        db_manager.disconnect()

if __name__ == "__main__":
    main() 