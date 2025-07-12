-- SQLite Schema for Business Data

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    age INTEGER,
    gender TEXT CHECK(gender IN ('M', 'F')),
    income_level TEXT CHECK(income_level IN ('Low', 'Medium', 'High')),
    customer_segment TEXT CHECK(customer_segment IN ('Bronze', 'Silver', 'Gold', 'Platinum')),
    registration_date TEXT
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    brand TEXT,
    price REAL CHECK(price > 0),
    cost REAL CHECK(cost > 0),
    inventory INTEGER DEFAULT 0,
    supplier_id INTEGER
);

-- Regions table
CREATE TABLE IF NOT EXISTS regions (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT NOT NULL,
    country TEXT,
    population INTEGER
);

-- Suppliers table
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    contact_person TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    rating REAL CHECK(rating >= 0 AND rating <= 5)
);

-- Sales table
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY,
    sale_date TEXT NOT NULL,
    product_id INTEGER,
    customer_id INTEGER,
    region_id INTEGER,
    quantity INTEGER CHECK(quantity > 0),
    unit_price REAL CHECK(unit_price > 0),
    total_amount REAL CHECK(total_amount > 0),
    FOREIGN KEY (product_id) REFERENCES products (product_id),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
    FOREIGN KEY (region_id) REFERENCES regions (region_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_product ON sales(product_id);
CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_sales_region ON sales(region_id);
CREATE INDEX IF NOT EXISTS idx_customers_segment ON customers(customer_segment);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category); 