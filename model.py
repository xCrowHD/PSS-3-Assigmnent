import sqlite3
import os
from datetime import datetime

DATABASE = 'database.db'

def create_tables():
    """Crea le tabelle degli eventi e delle categorie se non esistono"""
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        # Tabella eventi (con riferimento alla categoria)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                start TEXT NOT NULL,
                end TEXT,
                description TEXT,
                color TEXT,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        ''')
        # Tabella categorie
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        db.commit()

def get_all_events():
    """Restituisce tutti gli eventi, includendo la categoria (se esiste)"""
    with sqlite3.connect(DATABASE) as db:
        db.row_factory = sqlite3.Row
        cursor = db.execute('''
            SELECT e.id, e.title, 
                   datetime(e.start) as start, 
                   datetime(e.end) as end, 
                   e.description, e.color,
                   c.name as category
            FROM events e
            LEFT JOIN categories c ON e.category_id = c.id
        ''')
        return cursor.fetchall()

def add_event(title, start, end, description, color, category_id):
    """Aggiunge un nuovo evento con la categoria"""
    with sqlite3.connect(DATABASE) as db:
        cursor = db.execute(
            'INSERT INTO events (title, start, end, description, color, category_id) VALUES (?, ?, ?, ?, ?, ?)',
            (title, start, end, description, color, category_id)
        )
        db.commit()
        return cursor.lastrowid

def update_event(event_id, title, start, end, description, color, category_id):
    """Aggiorna un evento esistente"""
    with sqlite3.connect(DATABASE) as db:
        db.execute(
            'UPDATE events SET title=?, start=?, end=?, description=?, color=?, category_id=? WHERE id=?',
            (title, start, end, description, color, category_id, event_id)
        )
        db.commit()

def delete_event(event_id):
    """Elimina un evento"""
    with sqlite3.connect(DATABASE) as db:
        db.execute('DELETE FROM events WHERE id=?', (event_id,))
        db.commit()

def get_all_categories():
    """Restituisce tutte le categorie"""
    with sqlite3.connect(DATABASE) as db:
        db.row_factory = sqlite3.Row
        cursor = db.execute('SELECT * FROM categories ORDER BY name')
        return cursor.fetchall()

def add_category(name):
    """Aggiunge una nuova categoria"""
    with sqlite3.connect(DATABASE) as db:
        cursor = db.execute(
            'INSERT INTO categories (name) VALUES (?)',
            (name,)
        )
        db.commit()
        return cursor.lastrowid

def get_total_study_hours_by_category(start_date=None, end_date=None):
    """
    Restituisce i dati grezzi delle ore di studio per ciascuna categoria
    nell'intervallo di date fornito (start_date, end_date).
    """
    with sqlite3.connect(DATABASE) as db:
        db.row_factory = sqlite3.Row
        query = '''
            SELECT categories.name AS name, 
                   ROUND(sum((julianday(end) - julianday(start)) * 24), 2) as total_hours
            FROM events JOIN categories ON events.category_id = categories.id
            WHERE end IS NOT NULL
        '''
        params = []
        
        # Filtra per intervallo di date
        if start_date and end_date:
            query += " AND date(start) > date(?) AND date(start) <= date(?)"
            params.extend([start_date, end_date])

        query += " GROUP BY categories.name ORDER BY categories.name"
        
        cursor = db.execute(query, params)
        return cursor.fetchall()

