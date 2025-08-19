# temp_fix.py
import sqlite3
import os

# This file should be in the same directory as your db.sqlite3
DB_FILE = "db.sqlite3"

if not os.path.exists(DB_FILE):
    print(f"Error: Database file '{DB_FILE}' not found. Make sure this script is in the same folder as manage.py.")
else:
    try:
        print(f"Connecting to {DB_FILE}...")
        # Connect to the database
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        print("Attempting to drop table 'accounts_notification'...")
        # The SQL command to delete the table
        cursor.execute("DROP TABLE accounts_notification;")
        
        # Commit the change to save it
        connection.commit()
        print("--- SUCCESS: Table 'accounts_notification' was deleted. ---")

    except sqlite3.Error as e:
        print(f"--- ERROR: An error occurred: {e} ---")
        print("This might happen if the table doesn't exist, which is also okay.")
    
    finally:
        # Close the connection
        if 'connection' in locals() and connection:
            connection.close()
            print("Connection closed.")