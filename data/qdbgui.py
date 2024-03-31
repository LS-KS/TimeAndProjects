from PySide6.QtWidgets import QTableView, QApplication
from PySide6.QtSql import QSqlDatabase
from viewmodel.models import SqlQueryModel
from pathlib import Path

app = QApplication()
db_name = 'TestDB'
user = ''
password = ''
db_file = Path(__file__).resolve().parent / f"{db_name}.sqlite"
connection: QSqlDatabase = QSqlDatabase.addDatabase("QSQLITE", db_name)
connection.setDatabaseName(str(db_file))
if not connection.open(user, password):
    print("Error:", connection.lastError().text())

model = SqlQueryModel()
model.setQuery('SELECT * FROM topics', connection)

view = QTableView()
view.setModel(model)
view.show()
app.exec()