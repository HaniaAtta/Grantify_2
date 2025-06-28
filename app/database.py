import sqlite3
import os
import logging
import argparse
#db path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "grants.db")

def connect_db():
    return sqlite3.connect(DB_PATH)

def create_database():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS grants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_updated TEXT
        )
    ''')
    conn.commit()
    conn.close()


from datetime import datetime

def add_grant(grant_dict):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        url = grant_dict.get('url')
        status = grant_dict.get('status')

        if not url or not status:
            logging.warning(f"Invalid grant data: {grant_dict}")
            return

        c.execute("SELECT * FROM grants WHERE url = ?", (url,))
        existing_grant = c.fetchone()

        now = datetime.utcnow().isoformat()

        if existing_grant:
            c.execute("""
                UPDATE grants
                SET status = ?, last_updated = ?
                WHERE url = ?
            """, (status, now, url))
            logging.info(f"Grant updated: {url} - {status}")
        else:
            c.execute("""
                INSERT INTO grants (url, status, last_updated)
                VALUES (?, ?, ?)
            """, (url, status, now))
            logging.info(f"Grant added: {url} - {status}")

        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Error adding/updating grant: {str(e)}")


def get_grants():
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT id, url, status FROM grants ORDER BY id ASC")
        grants = c.fetchall()
        conn.close()
        return grants
    except Exception as e:
        logging.error(f"Error fetching grants: {str(e)}")
        return []

def url_exists(url):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT 1 FROM grants WHERE url = ?", (url,))
        exists = c.fetchone() is not None
        conn.close()
        return exists
    except Exception as e:
        logging.error(f"Error checking URL existence: {str(e)}")
        return False





def delete_grant(id_range_start, id_range_end):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Delete grants in the specified range
    cursor.execute("DELETE FROM grants WHERE id BETWEEN ? AND ?", (id_range_start, id_range_end))
    
    # Reset the auto-increment counter to the highest ID in the grants table
    cursor.execute("""
        UPDATE sqlite_sequence
        SET seq = (SELECT MAX(id) FROM grants)
        WHERE name = 'grants'
    """)
    
    conn.commit()
    conn.close()
    print(f"Deleted grants with IDs between {id_range_start} and {id_range_end} and reset the auto-increment counter.")

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Delete grants from the database")
    parser.add_argument("start_id", type=int, help="Start ID of the range")
    parser.add_argument("end_id", type=int, help="End ID of the range")

    # Parse arguments
    args = parser.parse_args()

    # Call delete_grant with the start and end IDs
    delete_grant(args.start_id, args.end_id)

def remove_grant_by_id(grant_id: int):
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute("DELETE FROM grants WHERE id = ?", (grant_id,))
        conn.commit()
        conn.close()
        print(f"[INFO] Grant with ID {grant_id} deleted.")
        return True
    except Exception as e:
        logging.error(f"Error deleting grant with ID {grant_id}: {str(e)}")
        return False

if __name__ == "__main__":
    main()