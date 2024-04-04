from pathlib import Path
import os
from PySide6.QtQml import QmlSingleton, QmlElement
from PySide6 import QtCore
from PySide6.QtSql import QSqlDatabase, QSqlQuery

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
@QmlSingleton
class DbController(QtCore.QObject):
    loginSuccess = QtCore.Signal(bool)
    logoutSuccess = QtCore.Signal()
    databaseName = QtCore.Signal(str)
    topicQueryChanged = QtCore.Signal(str, str)  # query, db_name
    topicStandardQuery = QtCore.Signal(bool)  # emit if not filtered to any topic
    entryQueryChanged = QtCore.Signal(str, str)  # query, db_name
    entrySaved = QtCore.Signal(int, str)  # record is, timestamp
    newYear = QtCore.Signal(int)
    topicDeleted = QtCore.Signal()
    username = QtCore.Signal(str)

    def __init__(self):
        super().__init__(None)
        self.db_name = ""
        self.year = QtCore.QDate.currentDate().year()
        self.db_columns = ['user', 'topic', 'description', 'year', 'date', 'start', 'end', 'duration']
        self.db_types = ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'TEXT', 'TEXT', 'TEXT', 'TEXT']

    @QtCore.Slot(str, str, str)
    def connect(self, db_name, user, password):
        # catch empty inputs
        if any([db_name == "", user == "", password == ""]):
            self.loginSuccess.emit(False)
            return
        # resolve database path
        db_file = Path(__file__).resolve().parent.parent / 'data' / f"{db_name}.sqlite"
        # establish a connection
        connection: QSqlDatabase = QSqlDatabase.addDatabase("QSQLITE", db_name)
        connection.setDatabaseName(str(db_file))
        # open the database
        if not connection.open(user, password):
            print("Error:", connection.lastError().text())
            self.loginSuccess.emit(False)
            return
        if connection.isOpen():
            self.db_name = db_name
            self.databaseName.emit(self.db_name)
            self.topicQueryChanged.emit('SELECT * FROM topics', db_name)
            self.entryQueryChanged.emit('SELECT * FROM timecapturing', db_name)
            self.username.emit(user)
            # get a list of all years
            actual_year = QtCore.QDate.currentDate().year()
            self.newYear.emit(actual_year)
            query = QSqlQuery(db=connection)
            query.prepare('SELECT year FROM timecapturing GROUP BY year')
            if not query.exec():
                print("Error executing query:", query.lastError().text())

            # Iterate over the results
            while query.next():
                year = query.value(0)
                print(f"query year: {year}")
                self.newYear.emit(year)

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
        creation_query += f"id INTEGER PRIMARY KEY, "
        for i, column in enumerate(self.db_columns):
            creation_query += f"{column} {self.db_types[i]}, "
        creation_query += ")"
        query = QSqlQuery(creation_query)
        query.exec()
        list_query = f"CREATE TABLE IF NOT EXISTS topics ("
        list_query += "id INTEGER PRIMARY KEY,"
        list_query += "topic VARCHAR(100) )"
        query = QSqlQuery(list_query)
        query.exec()
        db.close()
        return True

    @QtCore.Slot()
    def disconnect(self):
        QSqlDatabase.removeDatabase(self.db_name)
        self.db_name = ""
        self.logoutSuccess.emit()

    @QtCore.Slot(str)
    def updateEntryQuery(self, topic: str):
        if topic == "":
            self.entryQueryChanged.emit('SELECT * FROM timecapturing', self.db_name)
            self.topicQueryChanged.emit('SELECT * FROM topics', self.db_name)
            self.topicStandardQuery.emit(True)
        else:
            r_query = f"SELECT * FROM timecapturing WHERE topic = '{topic}'"
            # print(f"updateEntryQuery: {r_query}")
            self.entryQueryChanged.emit(r_query, self.db_name)
    @QtCore.Slot(int)
    def removeTopic(self, id):
        connection = QSqlDatabase().database(self.db_name)
        query = QSqlQuery(connection)
        query.prepare("DELETE FROM topics WHERE id = :id")
        query.bindValue(":id", id)
        if not query.exec():
            print("Error while deleting topic:", query.lastError().text())
        else:
            # print("Topic deleted successfully")
            self.topicDeleted.emit()

    @QtCore.Slot(int)
    def setYear(self, year):
        if self.db_name == "":
            return
        print(self.db_name)
        self.year = year
        self.topicQueryChanged.emit(
            f"SELECT  DISTINCT  topics.id, topics.topic  FROM topics INNER JOIN timecapturing ON topics.topic = timecapturing.topic WHERE timecapturing.year = {self.year} GROUP BY topics.topic",
            self.db_name)

    @QtCore.Slot(bool, int, str, str, str, str, str, str, str, str)
    def saveEntry(self, new_record:bool, record:int, user: str, topic: str, description: str, year: str, date: str, start: str, end: str, duration: str):
        connection = QSqlDatabase.database(self.db_name)
        if new_record: # create an insert query
            r_query = f"INSERT INTO timecapturing (user, topic, description, year, date, start, end, duration) VALUES ('{user}', '{topic}', '{description}', '{year}', '{date}', '{start}', '{end}', '{duration}');"
            insert_query = QSqlQuery(connection)
            insert_query.prepare(r_query)
            if not insert_query.exec():
                print("Error executing insert query:", insert_query.lastError().text())
            else:
                self.entrySaved.emit(insert_query.lastInsertId(), QtCore.QDateTime.currentDateTime().toString())
                self.updateEntryQuery(topic)
        else: # update query where id == record
            r_query = f"Update timecapturing SET user = '{user}', topic = '{topic}', description = '{description}', year = '{year}', date = '{date}', start = '{start}', end = '{end}', duration = '{duration}' WHERE id = {record};"
            update_query = QSqlQuery(connection)
            update_query.prepare(r_query)
            if not update_query.exec():
                print("Error executing update query:", update_query.lastError().text())
            else:
                self.entrySaved.emit(record, QtCore.QDateTime.currentDateTime().toString())
                self.updateEntryQuery(topic)
    @QtCore.Slot(str)
    def addTopic(self, topic: str):
        connection = QSqlDatabase.database(self.db_name)
        r_query = f"SELECT * FROM topics WHERE topic = '{topic}';"
        select_query = QSqlQuery(r_query, connection)
        if not select_query.exec():
            print("Error executing select query:", select_query.lastError().text())
        if select_query.next(): # return if topic in topics
            return
        # perform an insertion query
        r_query = f"INSERT INTO topics (topic) VALUES ('{topic}');"
        insert_query = QSqlQuery(r_query, connection)
        self.updateEntryQuery("")


    @QtCore.Slot()
    def discardEntry(self):
        pass
