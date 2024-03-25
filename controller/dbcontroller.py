from pathlib import Path
import os
from PySide6.QtQml import QmlSingleton, QmlElement
from PySide6 import QtCore
from PySide6.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1



@QmlElement
@QmlSingleton
class DbController(QtCore.QObject):
    loginSuccess = QtCore.Signal(bool)
    logoutSuccess = QtCore.Signal()
    def __init__(self):
        self.db_name = ""
        self.db_columns = ['user', 'topic', 'description', 'year', 'date', 'start', 'end', 'duration']
        self.db_types = ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'TEXT', 'TEXT', 'TEXT', 'TEXT']
        self._topicmodel = QSqlQueryModel()
        self._entrymodel = QSqlQueryModel()
        super().__init__(None)

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
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(str(db_file))
        db.setUserName(user)
        db.setPassword(password)
        if not db.open():
            print("Error:", db.lastError().text())
            self.loginSuccess.emit(False)
            return
        if db.isOpen():
            self.db_name = db_name
            self.loginSuccess.emit(True)
        else:
            self.loginSuccess.emit(False)

    @QtCore.Slot(str, result=bool)
    def check_database_name(self, db_name) -> bool:
        if db_name == "":
            return False
        db_file = Path(__file__).resolve().parent.parent / 'data' / f"{db_name}.sqlite"
        result = os.path.exists(db_file)
        return result

    @QtCore.Slot(str, str, str, result=bool)
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