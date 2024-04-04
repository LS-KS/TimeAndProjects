from typing import Union

from PySide6.QtCore import QModelIndex, QAbstractListModel
from PySide6.QtQml import QmlElement, QmlSingleton
from PySide6.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PySide6 import QtCore

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
@QmlSingleton
class TopicModel(QSqlQueryModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._roleNames = {}
        self.db_name = ""

    @QtCore.Slot(str, str)
    def setQuery(self, query: str, db: str):
        connection = QSqlDatabase().database(db)
        super().setQuery(query, connection)
        self.generateRoleNames()

    @QtCore.Slot(str)
    def setDatabaseName(self, db_name):
        self.db_name = db_name
    @QtCore.Slot(int, result=int)
    def idOf(self, row):
        index = self.index(row, 0)
        data = int(self.data(index, 0))
        #print(f"TopicModel::idOf {data = }")
        return data

    @QtCore.Slot(int, result=str)
    def topicOf(self, row):
        index = self.index(row, 1)
        data = str(self.data(index, 0))
        #print(f"TopicModel::topicOf {data = }")
        return data

    def generateRoleNames(self):
        self._roleNames = {}
        for i in range(super().record().count()):
            self._roleNames[QtCore.Qt.UserRole + i + 1] = super().record().fieldName(i)
        #print(f"TopicModel: generateRoleNames produced: {self._roleNames =}")

    def data(self, index:QModelIndex, role: int = ...):
        #print(f"TopicModel: data called with {index = }, {role = }")
        data = None
        if role < QtCore.Qt.UserRole:
            data = super().data(index, role)
        else:
            columnIdx = role - QtCore.Qt.UserRole - 1
            modelIndex = self.index(index.row(), columnIdx)
            data = super().data(modelIndex, QtCore.Qt.DisplayRole)
        return data


@QmlElement
@QmlSingleton
class EntryModel(QSqlQueryModel):
    emptyTopic = QtCore.Signal(bool) # emits True if empty topic is selected
    entryData = QtCore.Signal(int, str, str, str, int, str, str, str, str) # record_id, topic, username, description, year, date, start, end, duration
    def __init__(self, parent = None):
        super().__init__(parent)
        self._roleNames = {}
        self.db_name = ""

    @QtCore.Slot(int, result=int)
    def idOf(self, row):
        index = self.index(row, 0)
        data = int(self.data(index, 0))
        # print(f"TopicModel::idOf {data = }")
        return data

    @QtCore.Slot(int)
    def loadEntry(self, record_id: int) -> None:
        r_query = f"SELECT * FROM timecapturing WHERE id = {record_id}"
        print(f"EntryModel::loadEntry: {r_query = }")
        query = QSqlQuery(r_query, QSqlDatabase().database(self.db_name))
        if query.next():
            record_id = query.value(0)
            username = query.value(1)
            topic = query.value(2)
            description = query.value(3)
            year = query.value(4)
            date = query.value(5)
            start = query.value(6)
            end = query.value(7)
            duration = query.value(8)
            self.entryData.emit(record_id, topic, username, description, year, date, start, end, duration)
        else:
            print("EntryModel::loadEntry: No record found")

    @QtCore.Slot(str, str)
    def setQuery(self, query: str, db: str):
        connection = QSqlDatabase().database(db)
        super().setQuery(query, connection)
        self.generateRoleNames()
        select_query = QSqlQuery(query, connection)
        if not select_query.next():
            #print("Empty topic detected: ", query)
            self.emptyTopic.emit(True)
        else:
            self.emptyTopic.emit(False)

    @QtCore.Slot(str)
    def setDatabaseName(self, db_name):
        self.db_name = db_name


    def generateRoleNames(self):
        self._roleNames = {}
        for i in range(super().record().count()):
            self._roleNames[QtCore.Qt.UserRole + i + 1] = super().record().fieldName(i)
        #print(f"EntryModel: generateRoleNames produced: {self._roleNames =}")

    def data(self, index: QModelIndex, role: int = ...):
        #print(f"EntryModel: data called with {index = }, {role = }")
        data = None
        if role < QtCore.Qt.UserRole:
            data = super().data(index, role)
        else:
            columnIdx = role - QtCore.Qt.UserRole - 1
            modelIndex = self.index(index.row(), columnIdx)
            data = super().data(modelIndex, QtCore.Qt.DisplayRole)
        return data

@QmlElement
@QmlSingleton
class YearModel(QAbstractListModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._years = [str(QtCore.QDate.currentDate().year())]

    def rowCount(self, parent=QModelIndex()):
        return len(self._years)

    def data(self, index: QModelIndex, role: int = ...):
        if role == QtCore.Qt.UserRole + 1:
            #print(f"YearModel: data called with {index.row() = }, {role = }, about to return {self._years[index.row()]}")
            return self._years[index.row()]

    def roleNames(self):
        return {QtCore.Qt.UserRole + 1: b'year'}

    @QtCore.Slot(str)
    def addYear(self, year):
        if year in self._years:
            return
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.insertRow(0)
        self._years.append(year)
        self._years.sort(reverse=True)
        self.endInsertRows()
        self.dataChanged.emit(self.index(0), self.index(len(self._years)))