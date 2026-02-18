import pytest
import pandas as pd
import os
import sys
from src.etl import transform


@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    return pd.DataFrame({
        'order_id': [1, 2, 3, 4],
        'order_date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'],
        'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor'],
        'quantity': [2, '', None, 1],  # Missing values
        'unit_price': [100.0, 25.0, 50.0, 200.0]
    })


def test_revenue_column_exists_and_non_negative(sample_data):
    """Test that revenue column exists and has no negative values"""
    df_transformed = transform(sample_data)
    
    # Check revenue column exists
    assert 'revenue' in df_transformed.columns, "Revenue column should exist"
    
    # Check all revenue values are non-negative
    assert (df_transformed['revenue'] >= 0).all(), "All revenue values should be non-negative"
    
    # Check revenue calculation is correct
    expected_revenues = [200.0, 25.0, 50.0, 200.0]  # Missing quantity filled with 1
    actual_revenues = df_transformed['revenue'].tolist()
    assert actual_revenues == expected_revenues, f"Expected {expected_revenues}, got {actual_revenues}"


def test_missing_quantity_filled_with_one(sample_data):
    """Test that missing quantity values are filled with 1"""
    df_transformed = transform(sample_data)
    
    # Check that all quantity values are now integers
    assert df_transformed['quantity'].dtype == 'int', "Quantity column should be integer type"
    
    # Check that missing values are filled with 1
    expected_quantities = [2, 1, 1, 1]  # '' and None become 1
    actual_quantities = df_transformed['quantity'].tolist()
    assert actual_quantities == expected_quantities, f"Expected {expected_quantities}, got {actual_quantities}"
