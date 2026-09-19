import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "recruitment.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            candidate_email TEXT,
            job_title TEXT,
            match_score REAL,
            recommendation TEXT,
            evaluation_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_evaluation(candidate_name, candidate_email, job_title, match_score, recommendation, evaluation_dict):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO evaluations (candidate_name, candidate_email, job_title, match_score, recommendation, evaluation_data, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_name or "Unknown Candidate",
        candidate_email or "N/A",
        job_title or "General Role",
        match_score or 0.0,
        recommendation or "Pending",
        json.dumps(evaluation_dict),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def fetch_all_evaluations():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, candidate_name, candidate_email, job_title, match_score, recommendation, created_at FROM evaluations ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
