import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

DB_PATH = "lisa.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Sessions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Messages table
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT,
            node TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            meta TEXT, -- JSON string for extra data like plan, code, feedback
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_session(session_id: str, title: str = "New Chat"):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO sessions (id, title) VALUES (?, ?)', (session_id, title))
    conn.commit()
    conn.close()

def get_session(session_id: str):
    conn = get_db_connection()
    c = conn.cursor()
    session = c.execute('SELECT * FROM sessions WHERE id = ?', (session_id,)).fetchone()
    conn.close()
    return dict(session) if session else None

def get_all_sessions():
    conn = get_db_connection()
    c = conn.cursor()
    sessions = c.execute('SELECT * FROM sessions ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(s) for s in sessions]

def add_message(session_id: str, role: str, content: str, node: str = None, meta: Dict = None):
    conn = get_db_connection()
    c = conn.cursor()
    meta_json = json.dumps(meta) if meta else None
    c.execute('''
        INSERT INTO messages (session_id, role, content, node, meta)
        VALUES (?, ?, ?, ?, ?)
    ''', (session_id, role, content, node, meta_json))
    conn.commit()
    conn.close()

def get_messages(session_id: str):
    conn = get_db_connection()
    c = conn.cursor()
    messages = c.execute('SELECT * FROM messages WHERE session_id = ? ORDER BY id', (session_id,)).fetchall()
    conn.close()
    
    results = []
    for m in messages:
        msg = dict(m)
        if msg['meta']:
            msg['meta'] = json.loads(msg['meta'])
        results.append(msg)
    return results
