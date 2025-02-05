import sqlite3
import os
from datetime import datetime

DATABASE = 'database.db'

def create_table():
    """Crea la tabella degli eventi se non esiste"""
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                start TEXT NOT NULL,
                end TEXT,
                description TEXT,
                color TEXT
            )
        ''')
        db.commit()

def get_all_events():
    """Restituisce tutti gli eventi"""
    with sqlite3.connect(DATABASE) as db:
        db.row_factory = sqlite3.Row
        cursor = db.execute('''
            SELECT id, title, 
            datetime(start) as start, 
            datetime(end) as end, 
            description, color 
            FROM events
        ''')
        return cursor.fetchall()

def add_event(title, start, end, description, color):
    """Aggiunge un nuovo evento"""
    with sqlite3.connect(DATABASE) as db:
        cursor = db.execute(
            'INSERT INTO events (title, start, end, description, color) VALUES (?, ?, ?, ?, ?)',
            (title, start, end, description, color)
        )
        db.commit()
        return cursor.lastrowid

def update_event(event_id, title, start, end, description, color):
    """Aggiorna un evento esistente"""
    with sqlite3.connect(DATABASE) as db:
        db.execute(
            'UPDATE events SET title=?, start=?, end=?, description=?, color=? WHERE id=?',
            (title, start, end, description, color, event_id)
        )
        db.commit()

def delete_event(event_id):
    """Elimina un evento"""
    with sqlite3.connect(DATABASE) as db:
        db.execute('DELETE FROM events WHERE id=?', (event_id,))
        db.commit()