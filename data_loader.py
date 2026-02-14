import json
import os
from typing import List, Dict, Any
from database import Database

class DataLoader:
    def __init__(self, data_folder: str = "data"):
        self.data_folder = data_folder
        
    def load_json_files(self) -> List[Dict[str, Any]]:
        """Load all JSON files from data folder"""
        all_data = []
        
        if not os.path.exists(self.data_folder):
            print(f"Warning: {self.data_folder} folder not found. Creating empty folder.")
            os.makedirs(self.data_folder)
            return all_data
        
        json_files = [f for f in os.listdir(self.data_folder) if f.endswith('.json')]
        
        if not json_files:
            print(f"Warning: No JSON files found in {self.data_folder} folder.")
            return all_data
        
        for filename in json_files:
            filepath = os.path.join(self.data_folder, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Handle specific structure {"data": [...]}
                    if isinstance(data, dict) and 'data' in data and isinstance(data['data'], list):
                        data = data['data']
                        
                    # Handle both list and single object
                    if isinstance(data, list):
                        all_data.extend(data)
                    else:
                        all_data.append(data)
                print(f"Loaded {filename}: {len(data) if isinstance(data, list) else 1} records")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        
        return all_data
    
    def prepare_content(self, record: Dict[str, Any]) -> str:
        """Combine fields into searchable text"""
        content_parts = []
        
        # Common field names to search for
        text_fields = [
            'title', 'name', 'question', 'query',
            'description', 'content', 'text', 'body',
            'answer', 'response', 'summary',
            'category', 'tags', 'keywords'
        ]
        
        for field in text_fields:
            if field in record and record[field]:
                value = record[field]
                if isinstance(value, list):
                    content_parts.append(' '.join(str(v) for v in value))
                else:
                    content_parts.append(str(value))
        
        # If no common fields found, use all string values
        if not content_parts:
            for key, value in record.items():
                if key != 'id' and isinstance(value, (str, int, float)):
                    content_parts.append(str(value))
        
        return ' '.join(content_parts).strip()
    
    def load_into_database(self, db: Database) -> int:
        """Load JSON data into database"""
        records = self.load_json_files()
        
        if not records:
            print("No data to load. Database will be empty.")
            return 0
        
        loaded_count = 0
        for idx, record in enumerate(records):
            # Generate ID if not present
            record_id = record.get('id', f"record_{idx}")
            
            # Prepare searchable content
            content = self.prepare_content(record)
            
            if content:
                # Store original record as metadata
                metadata = json.dumps(record)
                if db.insert_record(record_id, content, metadata):
                    loaded_count += 1
        
        print(f"Successfully loaded {loaded_count} records into database")
        return loaded_count
