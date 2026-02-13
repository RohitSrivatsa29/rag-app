import sqlite3
import os
from typing import List, Dict, Any

class Database:
    def __init__(self, db_path: str = "knowledge.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        
    def create_table(self):
        """Create knowledge table if not exists"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                metadata TEXT
            )
        """)
        self.conn.commit()
        
    def insert_record(self, record_id: str, content: str, metadata: str = ""):
        """Insert a record, ignore if id already exists"""
        try:
            self.cursor.execute(
                "INSERT OR IGNORE INTO knowledge (id, content, metadata) VALUES (?, ?, ?)",
                (record_id, content, metadata)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting record {record_id}: {e}")
            return False
    
    def get_all_records(self) -> List[Dict[str, Any]]:
        """Get all records from database"""
        self.cursor.execute("SELECT id, content, metadata FROM knowledge")
        rows = self.cursor.fetchall()
        return [
            {"id": row[0], "content": row[1], "metadata": row[2]}
            for row in rows
        ]
    
    def get_record_by_id(self, record_id: str) -> Dict[str, Any]:
        """Get a specific record by id"""
        self.cursor.execute(
            "SELECT id, content, metadata FROM knowledge WHERE id = ?",
            (record_id,)
        )
        row = self.cursor.fetchone()
        if row:
            return {"id": row[0], "content": row[1], "metadata": row[2]}
        return None
    
    def count_records(self) -> int:
        """Count total records in database"""
        self.cursor.execute("SELECT COUNT(*) FROM knowledge")
        return self.cursor.fetchone()[0]
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
