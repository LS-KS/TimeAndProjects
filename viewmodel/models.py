from PySide6.QtCore import QAbstractListModel, QAbstractTableModel, QSortFilterProxyModel, QModelIndex, Signal, Slot
from PySide6.QtSql import QSqlQueryModel, QSqlRelationalTableModel, QSqlDatabase, QSqlQuery, QSqlRecord
from PySide6 import QtCore
from PySide6.QtGui import QFont

class entry_model(QSqlRelationalTableModel):

    def __init__(self):
        super().__init__()
        self._data = []
        self._headers = ['id', 'user', 'topic', 'description', 'year', 'date', 'start', 'end', 'duration']

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._headers)

    def roleNames(self):
        roles = {
            QtCore.Qt.UserRole: b'id',
            QtCore.Qt.UserRole + 1: b'user',
            QtCore.Qt.UserRole + 2: b'topic',
            QtCore.Qt.UserRole + 3: b'description',
            QtCore.Qt.UserRole + 4: b'year',
            QtCore.Qt.UserRole + 5: b'date',
            QtCore.Qt.UserRole + 6: b'start',
            QtCore.Qt.UserRole + 7: b'end',
            QtCore.Qt.UserRole + 8: b'duration'
        }
        return roles

    def data(self, index: QModelIndex, role: int = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if not 0 <= index.row() < len(self._data):
            return None
        if not 0 <= index.column() < len(self._headers):
            return None
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        if role == QtCore.Qt.UserRole:
            return self._data[index.row()][0]
        if role == QtCore.Qt.UserRole + 1:
            return self._data[index.row()][1]
        if role == QtCore.Qt.UserRole + 2:
            return self._data[index.row()][2]
        if role == QtCore.Qt.UserRole + 3:
            return self._data[index.row()][3]
        if role == QtCore.Qt.UserRole + 4:
            return self._data[index.row()][4]
        if role == QtCore.Qt.UserRole + 5:
            return self._data[index.row()][5]
        if role == QtCore.Qt.UserRole + 6:
            return self._data[index.row()][6]
        if role == QtCore.Qt.UserRole + 7:
            return self._data[index.row()][7]
        if role == QtCore.Qt.UserRole + 8:
            return self._data[index.row()][8]
        return None

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation ,  role: int):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal and 0 <= section < len(self._headers):
                print(f"headerData returns: {self._headers[section] = }")
                return self._headers[section]
        elif role == QtCore.Qt.FontRole and 0 <= section < len(self._headers):
            font = QFont()
            font.setBold(True);
            return font
        return None



class SqlQueryModel(QSqlQueryModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._roleNames = {}

    def setQuery(self, query: str, db: QSqlDatabase):
        super().setQuery(query, db)
        self.generateRoleNames()

    def generateRoleNames(self):
        self._roleNames = {}
        for i in range(super().record().count()):
            self._roleNames[QtCore.Qt.UserRole + i + 1] = super().record().fieldName(i)
        print(f"generateRoleNames produced: {self._roleNames =}")

    def data(self, index:QModelIndex, role: int = ...):
        print(f"data called with {index = }, {role = }")
        if role < QtCore.Qt.UserRole:
            print("if here")
            if not self.query().exec():
                print("Error while executing", self.query().lastError().text())
            i: int =0
            while self.query().next():
                data = self.query().value(index.column())
                if i == index.row(): break
                i +=1
        else:
            print("else here")
            columnIdx = role - QtCore.Qt.UserRole - 1
            modelIndex = self.index(index.row(), columnIdx)
            data = super().data(modelIndex, QtCore.Qt.DisplayRole)
        print(f"fetched data: {data =} ")
        return data


