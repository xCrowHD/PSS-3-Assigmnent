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

# Funzioni per ottenere i dati di studio aggregati per grafico

def get_daily_study_summary(start_date=None, end_date=None):
    """
    Restituisce la somma delle ore di studio per ogni giorno,
    filtrando gli eventi in base a start_date e end_date, se forniti.
    """
    with sqlite3.connect(DATABASE) as db:
        db.row_factory = sqlite3.Row
        query = '''
            SELECT date(start) as day, 
                   sum((julianday(end) - julianday(start)) * 24) as hours
            FROM events
            WHERE end IS NOT NULL
        '''
        params = []
        if start_date and end_date:
            query += " AND date(start) >= date(?) AND date(start) < date(?)"
            params.extend([start_date, end_date])
        query += " GROUP BY day ORDER BY day"
        cursor = db.execute(query, params)
        return cursor.fetchall()

def get_weekly_study_summary(start_date=None, end_date=None):
    """
    Restituisce la somma delle ore di studio per ogni settimana,
    filtrando gli eventi se start_date ed end_date sono forniti.
    """
    with sqlite3.connect(DATABASE) as db:
        db.row_factory = sqlite3.Row
        query = '''
            SELECT strftime('%Y-%W', start) as week, 
                   sum((julianday(end) - julianday(start)) * 24) as hours
            FROM events
            WHERE end IS NOT NULL
        '''
        params = []
        if start_date and end_date:
            query += " AND date(start) >= date(?) AND date(start) < date(?)"
            params.extend([start_date, end_date])
        query += " GROUP BY week ORDER BY week"
        cursor = db.execute(query, params)
        return cursor.fetchall()

def get_monthly_study_summary(start_date=None, end_date=None):
    """
    Restituisce la somma delle ore di studio per ogni mese,
    filtrando gli eventi se start_date ed end_date sono forniti.
    """
    with sqlite3.connect(DATABASE) as db:
        db.row_factory = sqlite3.Row
        query = '''
            SELECT strftime('%Y-%m', start) as month, 
                   sum((julianday(end) - julianday(start)) * 24) as hours
            FROM events
            WHERE end IS NOT NULL
        '''
        params = []
        if start_date and end_date:
            query += " AND date(start) >= date(?) AND date(start) < date(?)"
            params.extend([start_date, end_date])
        query += " GROUP BY month ORDER BY month"
        cursor = db.execute(query, params)
        return cursor.fetchall()

