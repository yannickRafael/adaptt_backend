import sqlite3
import os

DB_NAME = "adaptt.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    """Initializes the database with the required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            project_id TEXT PRIMARY KEY,
            project_name TEXT,
            status TEXT,
            data_raw TEXT,
            last_sync DATETIME,
            is_processed INTEGER DEFAULT 0,
            transparency_score INTEGER,
            alert_color TEXT,
            simple_message TEXT
        )
    ''')

    # Create project_documents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_documents (
            doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT,
            doc_type TEXT,
            is_published INTEGER DEFAULT 0,
            critical_weight REAL DEFAULT 0.0,
            FOREIGN KEY (project_id) REFERENCES projects (project_id)
        )
    ''')

    # Create locations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id TEXT PRIMARY KEY,
            name TEXT,
            region TEXT,
            country TEXT
        )
    ''')

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_number TEXT UNIQUE NOT NULL,
            region_id TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (region_id) REFERENCES locations (id)
        )
    ''')

    # Create subscriptions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            project_id TEXT NOT NULL,
            subscribed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            notification_enabled INTEGER DEFAULT 1,
            notification_channel TEXT DEFAULT 'sms' CHECK(notification_channel IN ('sms', 'wpp')),
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (project_id) REFERENCES projects (project_id),
            UNIQUE (user_id, project_id)
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database {DB_NAME} initialized successfully.")

def update_project_score(project_id, score_data):
    """Updates the project with the calculated score and alert message."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE projects
        SET transparency_score = ?,
            alert_color = ?,
            simple_message = ?,
            is_processed = 1
        WHERE project_id = ?
    ''', (score_data['transparency_score'], score_data['alert_color'], score_data['simple_message'], project_id))
    
    conn.commit()
    conn.close()

def get_unprocessed_projects():
    """Retrieves a list of project IDs that have not been processed yet."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT project_id FROM projects WHERE is_processed = 0')
    rows = cursor.fetchall()
    conn.close()
    
    return [row['project_id'] for row in rows]

if __name__ == "__main__":
    initialize_db()
