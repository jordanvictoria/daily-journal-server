import sqlite3
import json
from models import Mood


def get_all_moods():
    """Method docstring."""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.label
        FROM mood a
        """)

        moods = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            mood = Mood(row['id'], row['label'])

            moods.append(mood.__dict__)

    return moods

def get_single_mood(id):
    """Method docstring."""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.label
        FROM mood a
        WHERE a.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        mood = Mood(data['id'], data['label'])

        return mood.__dict__
