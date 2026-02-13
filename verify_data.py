from database import Database
import json

def verify():
    db = Database("knowledge.db")
    db.connect()
    
    count = db.count_records()
    print(f"Total records: {count}")
    
    records = db.get_all_records()
    print(f"Retrieved {len(records)} records.")
    
    # Check first 3 records
    for i, record in enumerate(records[:3]):
        print(f"\nRecord {i+1}:")
        print(f"ID: {record['id']}")
        print(f"Content (first 100 chars): {record['content'][:100]}...")
        if record['metadata']:
            try:
                meta = json.loads(record['metadata'])
                print(f"Metadata keys: {list(meta.keys())}")
            except:
                print("Metadata is not valid JSON")

    db.close()

if __name__ == "__main__":
    verify()
