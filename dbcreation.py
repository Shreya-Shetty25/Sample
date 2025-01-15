import pandas as pd
import sqlite3

# Load the CSV file into a DataFrame
csv_file = '/home/shreya-shetty/Documents/TASK 4 JAN 15/books.csv'  # Update this to your CSV file path
df = pd.read_csv(csv_file)

# Connect to SQLite database (it will create a new database file if it doesn't exist)
db_file = 'database.db'  # The SQLite database file
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Convert the DataFrame to SQL and save it to the database
table_name = 'book'  # Choose the table name
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"CSV file has been successfully converted to the database '{db_file}' in the table '{table_name}'.")
