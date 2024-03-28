from pathlib import Path
import os
from viewmodel.models import entry_model
from PySide6.QtQml import QmlSingleton, QmlElement
from PySide6 import QtCore
from PySide6.QtSql import QSqlQueryModel, QSqlRelationalTableModel, QSqlDatabase, QSqlQuery
from viewmodel.models import SqlQueryModel
QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1



@QmlElement
@QmlSingleton
class DbController(QtCore.QObject):
    loginSuccess = QtCore.Signal(bool)
    logoutSuccess = QtCore.Signal()
    def __init__(self):
        super().__init__(None)
        self.db_name = ""
        self.db_columns = ['user', 'topic', 'description', 'year', 'date', 'start', 'end', 'duration']
        self.db_types = ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'TEXT', 'TEXT', 'TEXT', 'TEXT']
        self._topicmodel = SqlQueryModel()
        self._entrymodel: QSqlRelationalTableModel = entry_model()


    @property
    def topicmodel(self):
        return self._topicmodel
    @property
    def entrymodel(self):
        return self._entrymodel
    @QtCore.Slot(str, str, str)
    def connect(self, db_name, user, password):
        if any([db_name == "", user == "", password == ""]):
            self.loginSuccess.emit(False)
            return
        db_file = Path(__file__).resolve().parent.parent / 'data' / f"{db_name}.sqlite"
        connection: QSqlDatabase = QSqlDatabase.addDatabase("QSQLITE", db_name)
        connection.setDatabaseName(str(db_file))
        if not connection.open(user, password):
            print("Error:", QSqlDatabase.lastError().text())
            self.loginSuccess.emit(False)
            return
        if connection.isOpen():
            self.db_name = db_name
            self._topicmodel.setQuery("SELECT topic FROM topics", db= connection)
            self._topicmodel.setHeaderData(0, QtCore.Qt.Horizontal, "id")
            self._topicmodel.setHeaderData(1, QtCore.Qt.Horizontal, "topic")
            self.loginSuccess.emit(True)
        else:
            self.loginSuccess.emit(False)

    @QtCore.Slot(str, result = bool)
    def check_database_name(self, db_name) -> bool:
        if db_name == "":
            return False
        db_file = Path(__file__).resolve().parent.parent / 'data' / f"{db_name}.sqlite"
        result = os.path.exists(db_file)
        return result

    @QtCore.Slot(str, str, str, result = bool)
    def create_database(self, db_name, user, password) -> bool:
        db_file = Path(__file__).resolve().parent.parent / 'data' / f"{db_name}.sqlite"
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(str(db_file))
        db.setUserName(user)
        db.setPassword(password)
        if not db.open():
            print("Error:", db.lastError().text())
            return False
        creation_query = f"CREATE TABLE IF NOT EXISTS timecapturing ("
        creation_query += f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
        for i, column in enumerate(self.db_columns):
            creation_query += f"{column} {self.db_types[i]}, "
        creation_query += ")"
        query = QSqlQuery(creation_query)
        query.exec()
        db.close()
        return True

    @QtCore.Slot()
    def disconnect(self):
        self._topicmodel.query().clear()
        self._topicmodel.clear()
        self._entrymodel.query().clear()
        self._entrymodel.clear()
        QSqlDatabase.removeDatabase(self.db_name)
        self.db_name = ""
        self.logoutSuccess.emit()


    @QtCore.Slot()
    def startEntry(self):
        pass

    @QtCore.Slot()
    def endEntry(self):
        pass

    @QtCore.Slot()
    def discardEntry(self):
        pass
