import sqlite3
import json
from models import Entry, Mood
from .tag_handler import get_single_tag


def get_all_entries():
    """Method docstring."""
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT DISTINCT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            a.date,
            m.label mood_label,
            (
            SELECT GROUP_CONCAT(t.id)
            FROM Entry_tag et JOIN Tag t ON et.tag_id = t.id
            WHERE et.entry_id = a.id
            ) as tags
        FROM entry a
        JOIN mood m
            ON m.id = a.mood_id
        LEFT OUTER JOIN Entry_tag et ON et.entry_id = a.id
        LEFT OUTER JOIN Tag t ON et.tag_id = t.id
        """)

        # Initialize an empty list to hold all entryrepresentations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entryinstance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # entryclass above.
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'], row['date'])
            mood = Mood(row['id'], row['mood_label'])
            tags = row['tags'].split(',') if row['tags'] else []
            entry_with_tags = []
            for tag in tags:
                tag_object = get_single_tag(tag)
                entry_with_tags.append(tag_object)
            entry.tags = entry_with_tags
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)

    return entries

def get_single_entry(id):
    """Method docstring."""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT DISTINCT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            a.date,
            (
            SELECT GROUP_CONCAT(t.id)
            FROM Entry_tag et JOIN Tag t ON et.tag_id = t.id
            WHERE et.entry_id = a.id
            ) as tags
        FROM entry a
        LEFT OUTER JOIN Entry_tag et ON et.entry_id = a.id
        LEFT OUTER JOIN Tag t ON et.tag_id = t.id
        WHERE a.id = ?;
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entryinstance from the current row
        entry = Entry (data['id'], data['concept'], data['entry'], data['mood_id'], data['date'])
        tags = data['tags'].split(',') if data['tags'] else []
        entry_with_tags = []
        for tag in tags:
            tag_object = get_single_tag(tag)
            entry_with_tags.append(tag_object)
        entry.tags = entry_with_tags

        return entry.__dict__

def get_entry_by_input(input):
    """Method docstring."""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.concept,
            a.entry,
            a.mood_id,
            a.date
        FROM entry a 
        WHERE a.entry LIKE ?
        """, ( f"%{input}%", ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'], row['date'])
            entries.append(entry.__dict__)

    return entries

def create_entry(new_entry):
    """Method docstring."""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT * 
                FROM Entry e
                LEFT OUTER JOIN Entry_Tag et 
                    ON e.id = et.entry_id
                LEFT OUTER JOIN Tag t
                    ON et.tag_id = t.id
            """)
        db_cursor.execute("""
        INSERT INTO entry
            ( concept, entry, mood_id, date )
        VALUES
            ( ?, ?, ?, ? );
        """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], new_entry['date'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the entrydictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = id

        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO Entry_Tag
                (entry_id, tag_id)
            VALUES
                (?, ?)
            """, (new_entry['id'], tag, ))


    return new_entry

def delete_entry(id):
    """Method docstring."""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entry
        WHERE id = ?
        """, (id, ))

def update_entry(id, new_entry):
    """Method docstring."""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE entry
            SET
                concept = ?,
                entry = ?,
                mood_id = ?,
                date = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['mood_id'], new_entry['date'], id, ))

        for tag in new_entry['tags']:
            db_cursor.execute("""
                DELETE FROM Entry_Tag
                WHERE entry_id = ?;
                """, (id, ))
        for tag in new_entry['tags']:
            db_cursor.execute("""
                INSERT INTO Entry_Tag
                    (entry_id, tag_id)
                VALUES
                    (?, ?);
                """, (new_entry['id'], tag))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
