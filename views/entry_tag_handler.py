import json
import sqlite3
from models import EntryTag
def get_all_entry_tags():
    """sql friendly function for getting all entry tags"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT t.id, t.tag_id, entry_id
        FROM Entry_Tag t;
        """)
        entry_tags = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry_tag = EntryTag(row['id'], row['tag_id'], row['entry_id'])
            entry_tags.append(entry_tag.__dict__)
    return entry_tags

def get_single_entry_tag(id):
    """sql friendly function for getting single entry tag"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT t.id, t.tag_id, t.entry_id
        FROM Entry_Tag t
            WHERE t.id = ? ;
        """, ( id,))
        data = db_cursor.fetchone()
        entry_tag = EntryTag(data['id'], data['tag_id'], data['entry_id'])
        return entry_tag.__dict__
