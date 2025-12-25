import sqlite3
from backend.config import DATABASE_FILE

def init_database():
    """Initializes the SQLite database and creates the necessary tables."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Create a table to store dataset metadata
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            table_name TEXT NOT NULL,
            is_cleaned BOOLEAN DEFAULT FALSE,
            source_dataset_id TEXT,
            FOREIGN KEY (source_dataset_id) REFERENCES datasets (id)
        )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")
