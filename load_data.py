from database import Database
from data_loader import DataLoader
import os

def main():
    # Initialize database
    db = Database("knowledge.db")
    db.connect()
    db.create_table()
    
    # Initialize data loader
    # Assuming data is in 'data' folder relative to this script
    data_folder = os.path.join(os.path.dirname(__file__), "data")
    loader = DataLoader(data_folder)
    
    # Load data
    print("Starting data ingestion...")
    count = loader.load_into_database(db)
    
    # Verify count
    total = db.count_records()
    print(f"Total records in database: {total}")
    
    db.close()

if __name__ == "__main__":
    main()
