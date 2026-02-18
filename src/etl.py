import pandas as pd
import sqlite3
import os
from datetime import datetime, timedelta
import random


def create_synthetic_data():
    """Create synthetic orders data if it doesn't exist"""
    os.makedirs('data/raw', exist_ok=True)
    
    if not os.path.exists('data/raw/orders.csv'):
        products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 
                   'Webcam', 'USB Cable', 'Desk Chair', 'Desk Lamp', 'Phone Case']
        
        data = []
        for i in range(1, 31):
            order_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
            product = random.choice(products)
            quantity = random.choice([random.randint(1, 5), '', '', None])  # Some missing values
            unit_price = round(random.uniform(10.0, 500.0), 2)
            
            data.append({
                'order_id': i,
                'order_date': order_date,
                'product': product,
                'quantity': quantity,
                'unit_price': unit_price
            })
        
        df = pd.DataFrame(data)
        df.to_csv('data/raw/orders.csv', index=False)
        print(f"Created synthetic data with {len(df)} rows")


def extract():
    """Extract data from CSV"""
    df = pd.read_csv('data/raw/orders.csv')
    return df


def transform(df):
    """Transform the data"""
    # Fill missing quantity with 1
    df['quantity'] = df['quantity'].fillna(1)
    df['quantity'] = df['quantity'].replace('', 1)
    
    # Convert data types
    df['quantity'] = df['quantity'].astype(int)
    df['unit_price'] = df['unit_price'].astype(float)
    
    # Create revenue column
    df['revenue'] = df['quantity'] * df['unit_price']
    
    return df


def load(df):
    """Load data to CSV and SQLite"""
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('db', exist_ok=True)
    
    # Write to CSV
    df.to_csv('data/processed/orders_clean.csv', index=False)
    
    # Write to SQLite
    conn = sqlite3.connect('db/orders.db')
    df.to_sql('orders_clean', conn, if_exists='replace', index=False)
    conn.close()


def calculate_kpis(df):
    """Calculate and print KPIs"""
    total_orders = len(df)
    total_revenue = df['revenue'].sum()
    top_product = df.groupby('product')['revenue'].sum().idxmax()
    
    print(f"\n=== KPIs ===")
    print(f"Total Orders: {total_orders}")
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Top Product by Revenue: {top_product}")


def main():
    """Main ETL pipeline"""
    print("Starting ETL pipeline...")
    
    # Create synthetic data if needed
    create_synthetic_data()
    
    # Extract
    print("Extracting data...")
    df = extract()
    
    # Transform
    print("Transforming data...")
    df_clean = transform(df)
    
    # Load
    print("Loading data...")
    load(df_clean)
    
    # Calculate KPIs
    calculate_kpis(df_clean)
    
    print("ETL pipeline completed successfully!")


if __name__ == "__main__":
    main()
