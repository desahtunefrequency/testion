import pandas as pd
import sqlite3

def process_excel_to_database(excel_file, database_file):
    """
    Reads an Excel file, cleans the data, and stores it into an SQLite database.

    Args:
        excel_file (str): Path to the Excel file.
        database_file (str): Path to the SQLite database file.
    """
    print("Starting data processing...")
    
    # Read the Excel file, skipping the first 4 rows
    df = pd.read_excel(excel_file, header=None, skiprows=4)
    print(f"Read {len(df)} rows from Excel, skipping first 4 rows.")
    
    # Use the first row as column names and remove it from DataFrame
    df.columns = df.iloc[0]
    df = df[1:]
    
    # Remove repeated header rows and summary rows
    df = df[df['Ident'] != 'Ident']
    df = df[df['Naziv'] != 'UKUPNO proizvod RN']
    
    data = []
    current_product_id = None
    
    for index, row in df.iterrows():
        first_col = str(row['Ident']).strip()
        
        if first_col.startswith('Proizvod RN:'):
            current_product_id = str(row.iloc[1]).strip()  # Access by index (second column)
        elif pd.notna(row['Količina']) and first_col != 'Ident' and first_col != 'nan':
            if current_product_id:
                ident = first_col
                name = str(row['Naziv']).strip() if pd.notna(row['Naziv']) else None
                quantity = float(row['Količina']) if pd.notna(row['Količina']) else 0
                data.append([current_product_id, ident, name, quantity])
            elif not current_product_id:
                ident = first_col
                name = str(row['Naziv']).strip() if pd.notna(row['Naziv']) else None
                quantity = float(row['Količina']) if pd.notna(row['Količina']) else 0
                data.append([None, ident, name, quantity])
    
    # Create the DataFrame
    output_df = pd.DataFrame(data, columns=['product_id', 'ident', 'name', 'quantity'])
    print("\nDataFrame created.")
    
    # Connect to SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products_materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            ident TEXT,
            name TEXT,
            quantity REAL
        )
    ''')
    print("Table created or already exists")
    
    # Insert the DataFrame into the SQLite table
    output_df.to_sql('products_materials', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()
    print("Data inserted into SQLite database.")
    print("\nData processing complete.")

# Example Usage
excel_file = "Obračun materijalnih potreba po identima.xls"  # Replace with your file name
database_file = "injection_data.db"  # Name of the SQLite database
process_excel_to_database(excel_file, database_file)