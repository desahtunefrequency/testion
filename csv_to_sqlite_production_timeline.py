import pandas as pd
import sqlite3

def read_csv_set_header_clean(csv_file):
    """
    Reads a CSV, sets the first valid row as the header, removes NaN rows,
    rows where the first element is "Strana", "Rok izr.", or contains "/",
    and inserts the cleaned data into an SQLite table.
    """
    try:
        df = pd.read_csv(csv_file, sep=';', encoding='windows-1250', header=None)
        
        # Find the first non-empty row (containing actual data for the header)
        header_index = -1
        for i in range(len(df)):
            if not df.iloc[i].isnull().all():
                header_row = df.iloc[i].tolist()
                df.columns = header_row
                header_index = i
                break
        
        if header_index == -1:
            print("Error: Could not find a valid header row.")
            return None
        
        df = df[header_index + 1:]  # Remove rows before and including the header
        df.reset_index(drop=True, inplace=True)
        
        # Remove rows with all NaN values
        df.dropna(how='all', inplace=True)
        
        # Remove rows where the first column's value is "Strana" or "Rok izr."
        df = df[df.iloc[:, 0].str.strip() != "Strana"]
        df = df[df.iloc[:, 0].str.strip() != "Rok izr."]
        
        # Remove rows where the first column contains "/"
        df = df[~df.iloc[:, 0].astype(str).str.contains("/")]
        
        df.reset_index(drop=True, inplace=True)
        
        # Insert data into SQLite table
        conn = sqlite3.connect('injection_data.db')
        df.to_sql('production_timeline', conn, if_exists='replace', index=False)
        conn.close()
        
        print("Data successfully inserted into 'production_timeline' table in 'injection_data.db'")
        return df
    
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return None
    except pd.errors.ParserError:
        print(f"Error: Could not parse CSV file '{csv_file}'. Check the file format.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Example usage:
csv_file = "Obračun proizvodnje_1.csv"
df = read_csv_set_header_clean(csv_file)