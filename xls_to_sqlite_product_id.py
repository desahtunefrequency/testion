import pandas as pd
import sqlite3

def insert_products_from_excel(excel_file):
    """
    Reads product data from an Excel file and inserts it into the 'products' table in the database.
    """
    try:
        # Read the Excel file (adjust sheet name if needed)
        df = pd.read_excel(excel_file, sheet_name='Sheet1')  # Assuming data is on 'Sheet1'
        
        # Rename columns to match your database table (IMPORTANT!)
        df = df.rename(columns={
            'proizvod': 'product_id',
            'naziv': 'name',
            'kol': 'made_qty'
            })
        
        # Select only the required columns
        df = df[['product_id', 'name', 'made_qty']]
        
        # Remove rows with empty product_id
        df = df.dropna(subset=['product_id'])
        
        # Convert product_id to string with leading zeros
        df['product_id'] = df['product_id'].astype(int).astype(str).str.zfill(6)
        
        # Insert data into SQLite table
        conn = sqlite3.connect('injection_data.db')
        df.to_sql('products', conn, if_exists='replace', index=False)  # Use 'append' if needed
        conn.close()
        
        print("Product data successfully inserted into 'products' table.")
    
    except FileNotFoundError:
        print(f"Error: File '{excel_file}' not found.")
    except pd.errors.ParserError:
        print(f"Error: Could not parse Excel file '{excel_file}'. Check the file format.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
excel_file = "Postkalkulacija - sumarno po proizvodima.xls"
insert_products_from_excel(excel_file)