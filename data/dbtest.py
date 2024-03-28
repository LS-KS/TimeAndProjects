import sqlite3

# Open a connection to the SQLite database
conn = sqlite3.connect('TestDB.sqlite')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a SELECT query to fetch data from the 'topics' table
cursor.execute("SELECT * FROM topics")

# Fetch all rows returned by the query
rows = cursor.fetchall()

# Iterate over the rows and print each row
for row in rows:
    print(row)

# Close the cursor and the database connection
cursor.close()
conn.close()

