from PySide6.QtCore import QModelIndex
from PySide6.QtQml import QmlElement, QmlSingleton
from PySide6.QtSql import QSqlQueryModel, QSqlDatabase
from PySide6 import QtCore

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
@QmlSingleton
class TopicModel(QSqlQueryModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._roleNames = {}

    @QtCore.Slot(str, str)
    def setQuery(self, query: str, db: str):
        connection = QSqlDatabase().database(db)
        super().setQuery(query, connection)
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
            data = super().data(index, role)
        else:
            columnIdx = role - QtCore.Qt.UserRole - 1
            modelIndex = self.index(index.row(), columnIdx)
            data = super().data(modelIndex, QtCore.Qt.DisplayRole)
        return data


