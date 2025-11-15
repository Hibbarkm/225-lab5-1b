import sqlite3

# Database file path (same as in your Flask app)
DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def clear_test_parts():
    """Clear only the test parts from the database."""
    db = connect_db()
    # Assuming all test parts follow a specific naming pattern
    db.execute("DELETE FROM parts WHERE name LIKE 'Test Part %'")
    db.commit()
    print('Test parts have been deleted from the database.')
    db.close()

if __name__ == '__main__':
    clear_test_parts()

