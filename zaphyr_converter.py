import pandas as pd
import sqlite3

def convert_to_sqlite(filepath, db_name, table_name):
    """
    Pretvara konfiguracijsku datoteku u SQLite tablicu.

    Args:
        filepath: Putanja do konfiguracijske datoteke.
        db_name: Ime SQLite baze podataka (npr. "moja_baza.db").
        table_name: Ime tablice u koju će se spremiti podaci.
    """
    
    try:
        # Učitavanje podataka iz datoteke u pandas DataFrame
        # Pokušaj s CP-1250 enkodiranjem, preskačući neispravne linije
        try:
            df = pd.read_csv(filepath, sep=",", header=None, names=["Parametar", "Vrijednost", "Jedinica", "Range_Min", "Range_Max", "Ostalo"], encoding="cp1250", on_bad_lines='skip')
        except UnicodeDecodeError:
            # Ako CP-1250 ne uspije, pokušaj s ISO-8859-2
            df = pd.read_csv(filepath, sep=",", header=None, names=["Parametar", "Vrijednost", "Jedinica", "Range_Min", "Range_Max", "Ostalo"], encoding="iso-8859-2", on_bad_lines='skip')
        
        # Uklanjanje praznih redova ako ih ima
        df.dropna(how='all', inplace=True)
        
        # Uklanjanje redaka koji ne sadrže validne podatke. Npr. redovi koji sadrže MOLD INFO, VE, CRC i sl.
        df = df[df['Parametar'].str.contains(r'\.')]
        
        # Kreiranje konekcije na SQLite bazu
        conn = sqlite3.connect(db_name)
        
        # Spremanje DataFrame-a u SQLite tablicu
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        
        # Zatvaranje konekcije
        conn.close()
        
        print(f"Datoteka '{filepath}' uspješno pretvorena u SQLite tablicu '{table_name}' u bazi '{db_name}'.")
    
    except FileNotFoundError:
        print(f"Greška: Datoteka '{filepath}' nije pronađena.")
    except Exception as e:
        print(f"Greška prilikom konverzije: {e}")

# Primjer korištenja
filepath = "PRE37.dat"  # Zamijeni s putanjom do tvoje datoteke
db_name = "stroj.db.sql"
table_name = "parametri_stroja"


convert_to_sqlite(filepath, db_name, table_name)