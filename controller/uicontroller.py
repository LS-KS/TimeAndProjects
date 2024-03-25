from PySide6.QtQml import QmlSingleton, QmlElement
from PySide6 import QtCore

QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
@QmlSingleton
class UiController(QtCore.QObject):

    def __init__(self):
        super().__init__(None)