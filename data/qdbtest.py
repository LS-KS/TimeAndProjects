from PySide6.QtSql import QSqlQuery, QSqlDatabase

# Set the database name
db_name = 'TestDB.sqlite'

# Add the database connection
db = QSqlDatabase.addDatabase('QSQLITE', db_name)
db.setDatabaseName(db_name)

if not db.open():
    print("Error while opening database:", db.lastError().text())

# Execute the query
query = QSqlQuery(db=db)
query.prepare('SELECT * FROM topics')

# Check if the query is valid
if not query.exec():
    print("Error executing query:", query.lastError().text())

# Iterate over the results
while query.next():
    id = query.value(0)
    topic = query.value(1)
    print(f"ID: {id}, Topic: {topic}")

# Close the database connection
db.close()
db.removeDatabase(db_name)
