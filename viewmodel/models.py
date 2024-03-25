from PySide6.QtCore import QAbstractListModel, QAbstractTableModel, QSortFilterProxyModel, QModelIndex Signal, Slot
from PySide6 import QtCore


class entry_model(QAbstractTableModel):

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

    def headerData(section: int, orientation: QtCore.Qt.Orientation ,  role: int):
    if (role == Qt::DisplayRole):
        if (orientation == Qt::Horizontal & & section >= 0 & & section < this->headers.size()):
            return this->headers[section];
    elif (role == Qt::FontRole & & section >= 0 & & section < this->headers.size()):
        QFont font;
        font.setBold(true);
        return font;
    return QVariant();
