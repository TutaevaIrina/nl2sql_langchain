import os
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import text
from pathlib import Path

# Get the base directory (project root) and data folder path
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Define connection URLs for each database
DATABASES = {
    "crimes": sa.URL.create("mysql+pymysql", username="root", password="nl2sql", host="localhost", port=3306, database="crimes"),
    "hospitality": sa.URL.create("mysql+pymysql", username="root", password="nl2sql", host="localhost", port=3306, database="hospitality"),
    "happiness": sa.URL.create("mysql+pymysql", username="root", password="nl2sql", host="localhost", port=3306, database="happiness"),
}

# Create databases if they don't exist
def create_databases():
    print("Creating databases if they don't exist...")
    admin_url = sa.URL.create("mysql+pymysql", username="root", password="nl2sql", host="localhost", port=3306)
    engine = sa.create_engine(admin_url)

    with engine.connect() as conn:
        for db_name in DATABASES:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
            
# Load crime dataset from CSV and store into the 'crimes' database
def load_crimes():
    print("Loading crime data...")
    engine = sa.create_engine(DATABASES["crimes"])
    csv_path = DATA_DIR / "crimes" / "crimes-2001-to-present.csv"
    df = pd.read_csv(csv_path)
    df.rename(columns={
        "ID": "id",
        "Case Number": "case_number",
        "Date": "date",
        "Block": "block",
        "IUCR": "iucr",
        "Primary Type": "primary_type",
        "Description": "description",
        "Location Description": "location_description",
        "Arrest": "arrest",
        "Domestic": "domestic",
        "Beat": "beat",
        "District": "district",
        "Ward": "ward",
        "Community Area": "community_area",
        "FBI Code": "fbi_code",
        "X Coordinate": "x_coordinate",
        "Y Coordinate": "y_coordinate",
        "Year": "year",
        "Updated On": "updated_on",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Location": "location",
    },
    inplace=True,
)
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y %I:%M:%S %p")
    df["updated_on"] = pd.to_datetime(df["updated_on"], format="%m/%d/%Y %I:%M:%S %p")
    df.rename(columns=lambda x: x.strip().lower().replace(" ", "_").replace("-", "_"), inplace=True)
    df.to_sql("crime_data", con=engine, if_exists="replace", index=False)
    print("Crime data loaded")


# Load happiness report data (2015–2019) into the 'happiness' database
def load_happiness():
    print("Loading happiness data...")
    engine = sa.create_engine(DATABASES["happiness"])
    path = DATA_DIR / "happiness"
    files = ["2015.csv", "2016.csv", "2017.csv", "2018.csv", "2019.csv"]

    for file in files:
        year = file[:4]
        df = pd.read_csv(path / file)

        # Normalize and rename inconsistent column names across years
        df.rename(columns={
            'Country': 'country',
            'Country or region': 'country',
            'Region': 'region',
            'Happiness Rank': 'happiness_rank',
            'Happiness.Rank': 'happiness_rank',
            'Overall rank': 'happiness_rank',
            'Happiness Score': 'happiness_score',
            'Happiness.Score': 'happiness_score',
            'Score': 'happiness_score',
            'Lower Confidence Interval': 'lower_confidence_interval',
            'Upper Confidence Interval': 'upper_confidence_interval',
            'Whisker.high': 'whisker_high',
            'Whisker.low': 'whisker_low',
            'Standard Error': 'standard_error',
            'Economy (GDP per Capita)': 'economy',
            'Economy..GDP.per.Capita.': 'economy',
            'GDP per capita': 'economy',
            'Family': 'family',
            'Social support': 'family',
            'Health (Life Expectancy)': 'health',
            'Health..Life.Expectancy.': 'health',
            'Healthy life expectancy': 'health',
            'Freedom': 'freedom',
            'Freedom to make life choices': 'freedom',
            'Trust (Government Corruption)': 'trust',
            'Trust..Government.Corruption.': 'trust',
            'Perceptions of corruption': 'trust',
            'Generosity': 'generosity',
            'Dystopia Residual': 'dystopia_residual',
            'Dystopia.Residual': 'dystopia_residual'
        }, inplace=True)

        # Store yearly happiness data in separate tables
        df.to_sql(name=f"happiness_{year}", con=engine, if_exists="replace", index=False)
        print(f"Year {year} loaded")

    print("Happiness data loaded")

# Load hospitality-related CSV files into the 'hospitality' database
def load_hospitality():
    print("Loading hospitality data...")
    engine = sa.create_engine(DATABASES["hospitality"])
    path = DATA_DIR / "hospitality"
    
    def load_and_insert(file, table, date_cols=None):
        csv_path = path / file
        if not csv_path.exists():
            raise FileNotFoundError(f"{csv_path} nicht gefunden")
        
        df = pd.read_csv(csv_path)
      
        date_cols = date_cols or []
        present = [c for c in date_cols if c in df.columns]
        for col in present:
            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"               
            )
        
        df.to_sql(table, con=engine, if_exists="replace", index=False)
        print(f"Loaded: {table} ({len(df)} rows)")

    load_and_insert("dim_date.csv", "dim_date", ["date"])
    load_and_insert("dim_hotels.csv", "dim_hotels")
    load_and_insert("dim_rooms.csv", "dim_rooms")
    load_and_insert("fact_aggregated_bookings.csv", "fact_aggregated_bookings", ["check_in_date"])    
    load_and_insert("fact_bookings.csv", "fact_bookings",
                    ["check_in_date", "booking_date", "check_out_date"])

    print("Hospitality data loaded")


# Main entry point to execute all tasks
def main():
    create_databases()    
    load_hospitality()
    load_happiness()

if __name__ == "__main__":
    main()
