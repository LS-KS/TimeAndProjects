from PySide6.QtCore import QAbstractListModel, QModelIndex
from PySide6.QtSql import QSqlQueryModel, QSqlDatabase, QSqlQuery
from PySide6 import QtCore

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
        print(f"SqlQueryModel: generateRoleNames produced: {self._roleNames =}")

    def data(self, index:QModelIndex, role: int = ...):
        print(f"SqlQueryModel: data called with {index = }, {role = }")
        data = None
        if role < QtCore.Qt.UserRole:
            data = super().data(item = index, role=role)
        else:
            columnIdx = role - QtCore.Qt.UserRole - 1
            modelIndex = self.index(index.row(), columnIdx)
            data = super().data(modelIndex, QtCore.Qt.DisplayRole)
        return data


