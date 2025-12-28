"""
Database module for storing food tracking entries.
"""
import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager


class Database:
    """Handles database operations for the fitness tracker."""
    
    def __init__(self, db_path='data/fitness_tracker.db'):
        """Initialize the database connection."""
        self.db_path = db_path
        self._ensure_data_directory()
        self._initialize_database()
    
    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        data_dir = os.path.dirname(self.db_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _initialize_database(self):
        """Create the database schema if it doesn't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS food_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    food_name TEXT NOT NULL,
                    calories REAL NOT NULL,
                    protein REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON food_entries(timestamp)
            ''')
    
    def add_entry(self, food_name, calories, protein):
        """Add a new food entry to the database."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO food_entries (food_name, calories, protein, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (food_name, calories, protein, timestamp))
        
        return cursor.lastrowid
    
    def get_all_entries(self):
        """Retrieve all food entries from the database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, food_name, calories, protein, timestamp
                FROM food_entries
                ORDER BY timestamp DESC
            ''')
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_daily_stats(self):
        """Get statistics for today's entries."""
        today = datetime.now().strftime('%Y-%m-%d')
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    COUNT(*) as count,
                    SUM(calories) as calories,
                    SUM(protein) as protein
                FROM food_entries
                WHERE DATE(timestamp) = ?
            ''', (today,))
            
            row = cursor.fetchone()
            if row and row['count'] > 0:
                return {
                    'count': row['count'],
                    'calories': round(row['calories'], 2),
                    'protein': round(row['protein'], 2)
                }
            return None
    
    def clear_all_entries(self):
        """Clear all entries from the database (for testing purposes)."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM food_entries')
