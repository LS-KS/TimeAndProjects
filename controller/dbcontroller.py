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
    holidayQueryChanged = QtCore.Signal(str, str)  # query, db_name
    publicHolidayQueryChanged = QtCore.Signal(str, str)  # query, db_name
    sickdayQueryChanged = QtCore.Signal(str, str)  # query, db_name
    entrySaved = QtCore.Signal(int, str)  # record is, timestamp
    newYear = QtCore.Signal(int)
    topicDeleted = QtCore.Signal()
    username = QtCore.Signal(str)
    metadata = QtCore.Signal(str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str,)
    usedHolidays = QtCore.Signal(float)
    holidayEntitlement = QtCore.Signal(float)
    publicHolidayCount = QtCore.Signal(float)
    sickDayCount = QtCore.Signal(float)
    holidayEntry = QtCore.Signal(int, str, str, str)
    holidayEntrySaved = QtCore.Signal(bool)
    holidayEntryDeleted = QtCore.Signal(bool)
    holidayEntryDuplicate = QtCore.Signal(int)
    holidayEntryNew = QtCore.Signal(int)
    publicHolidayEntry = QtCore.Signal(int, str, str, str, str)
    sickdayEntry = QtCore.Signal(int, str, str, str)

    def __init__(self):
        super().__init__(None)
        self.holidays = 0
        self.db_name = ""
        self.year = QtCore.QDate.currentDate().year()
        self.weekly_hours : float = 0
        self.daily_hours : float = 0
        self.db_columns = ['user', 'topic', 'description', 'year', 'date', 'start', 'end', 'duration']
        self.db_types = ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'TEXT', 'TEXT', 'TEXT', 'TEXT']

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
            self.updateEntryQuery("")
            self.username.emit(user)
            # get a list of all years
            actual_year = QtCore.QDate.currentDate().year()
            self.newYear.emit(actual_year)
            query = QSqlQuery(db=connection)
            query.prepare('SELECT year FROM timecapturing GROUP BY year Order BY year DESC, date')
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
        self.load_metadata()

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
        self._create_metatables(db)
        db.close()
        return True

    @QtCore.Slot(int)
    def deleteHolidayEntry(self, id):
        del_query = f"DELETE FROM holidays WHERE id = {id}"
        query = QSqlQuery(del_query, QSqlDatabase().database(self.db_name))
        self.holidayEntryDeleted.emit(query.exec())
    def _create_metatables(self, connection: QSqlDatabase) -> None:
        meta_query = """CREATE TABLE  IF NOT EXISTS `meta` (
                            'company_name' TEXT,
                            'company_street' TEXT,
                            'company_city' TEXT,
                            'company_zip' TEXT,
                            'company_email' TEXT,
                            'company_phone' TEXT,
                            'employee_name' TEXT,
                            'employee_street' TEXT,
                            'employee_city' TEXT,
                            'employee_zip' TEXT,
                            'employee_email' TEXT,
                            'employee_phone' TEXT,
                            'employee_id' TEXT,
                            'employee_holiday_entitlement' TEXT,
                            'employee_weekly_hours' TEXT,
                            'employee_daily_hours' TEXT
                            );"""
        holiday_query = """CREATE TABLE  IF NOT EXISTS `holidays` (
                            'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                            'year' INTEGER,
                            'day' TEXT,
                            'hours' TEXT
                            );"""
        public_holiday_query = """CREATE TABLE  IF NOT EXISTS `public_holidays` (
                                    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                                    'year' INTEGER,
                                    'day' TEXT,
                                    'description' TEXT,
                                    'hours' TEXT
                                    );"""
        sick_query = """CREATE TABLE  IF NOT EXISTS `sickdays` (
                        'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                        'year' INTEGER,
                        'day' TEXT,
                        'hours' TEXT
                        );"""
        for querytext in [meta_query, holiday_query, public_holiday_query, sick_query]:
            query = QSqlQuery(querytext, connection)
            if not query.exec():
                print(f"Error while creating metatable {querytext}:", query.lastError().text())
    @QtCore.Slot()
    def discardEntry(self):
        pass

    @QtCore.Slot()
    def disconnect(self):
        QSqlDatabase.removeDatabase(self.db_name)
        self.db_name = ""
        self.logoutSuccess.emit()
    @QtCore.Slot(result = str)
    def getDailyHours(self):
        hours = self.daily_hours//1
        minutes = (self.daily_hours - hours) * 60
        seconds = (minutes - int(minutes)) * 60
        hours: str = str(hours if hours > 9 else "0" + str(int(hours)))
        minutes: str = str(int(minutes) if minutes > 9 else "0" + str(int(minutes)))
        seconds: str = str(int(seconds) if seconds > 9 else "0" + str(int(seconds)))
        return str( hours + ":" + minutes + ":" + seconds)
    @QtCore.Slot()
    def getUsedHolidays(self):
        r_query = f"SELECT hours FROM holidays WHERE year = '{self.year}'"
        query = QSqlQuery(r_query, QSqlDatabase().database(self.db_name))
        hours = []
        if not query.exec():
            print("Error executing query:", query.lastError().text())
            return
        while query.next():
            hours.append(query.value(0))
        hour_sum = 0
        for time_string in hours:
            if len(time_string.split(":")) == 3:
                hour_sum += int(time_string.split(":")[0]) + int(time_string.split(":")[1])/60 + int(time_string.split(":")[2])/3600
        self.usedHolidays.emit(hour_sum/self.daily_hours)
        self.holidayEntitlement.emit(self.holidays)

    @QtCore.Slot()
    def getPublicHolidayCount(self):
        r_query = f"SELECT hours FROM public_holidays WHERE year = '{self.year}'"
        query = QSqlQuery(r_query, QSqlDatabase().database(self.db_name))
        if not query.exec():
            print("Error executing query:", query.lastError().text())
            return
        hours = []
        while query.next():
            hours.append(query.value(0))
        hour_sum = 0
        for time_string in hours:
            if len(time_string.split(":")) == 3:
                hour_sum += int(time_string.split(":")[0]) + int(time_string.split(":")[1])/60 + int(time_string.split(":")[2])/3600
        self.publicHolidayCount.emit(hour_sum/self.daily_hours)

    @QtCore.Slot()
    def getSickDayCount(self):
        r_query = f"SELECT hours FROM sickdays WHERE year = '{self.year}'"
        query = QSqlQuery(r_query, QSqlDatabase().database(self.db_name))
        if not query.exec():
            print("Error executing query:", query.lastError().text())
            return
        hours = []
        while query.next():
            hours.append(query.value(0))
        hour_sum = 0
        for time_string in hours:
            if len(time_string.split(":")) == 3:
                hour_sum += int(time_string.split(":")[0]) + int(time_string.split(":")[1])/60 + int(time_string.split(":")[2])/3600
        self.sickDayCount.emit(hour_sum/self.daily_hours)

    @QtCore.Slot()
    def load_metadata(self) -> None:
        r_query = "SELECT * FROM meta"
        query = QSqlQuery(r_query, QSqlDatabase().database(self.db_name))
        if not query.exec():
            print("Error executing query:", query.lastError().text())
            return
        while query.next():
            company_name = query.value(0)
            companyStreet = query.value(1)
            companyCity = query.value(2)
            companyZip = query.value(3)
            companyEmail = query.value(4)
            companyPhone = query.value(5)

            employeeName = query.value(6)
            employeeStreet = query.value(7)
            employeeCity = query.value(8)
            employeeZip = query.value(9)
            employeeEmail = query.value(10)
            employeePhone = query.value(11)
            employeeId = query.value(12)
            holidays = query.value(13)
            weeklyHours = query.value(14)
            dailyHours = query.value(15)
            self.metadata.emit(
                company_name,
                companyStreet,
                companyCity,
                companyZip,
                companyEmail,
                companyPhone,
                employeeName,
                employeeStreet,
                employeeCity,
                employeeZip,
                employeeEmail,
                employeePhone,
                employeeId,
                holidays,
                weeklyHours,
                dailyHours,
            )
            self.holidays = float(holidays)
            self.weekly_hours = float(weeklyHours)
            self.daily_hours = float(dailyHours)

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
        self.holidayQueryChanged.emit(f"SELECT * FROM holidays WHERE year = {self.year}", self.db_name)
        self.publicHolidayQueryChanged.emit(f"SELECT * FROM public_holidays WHERE year = {self.year}", self.db_name)
        self.sickdayQueryChanged.emit(f"SELECT * FROM sickdays WHERE year = {self.year}", self.db_name)

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

    @QtCore.Slot(int, str, str, str)
    def saveHolidayEntry(self, id, day, hours, year):
        # check if there is an entry with the same day
        r_query = f"SELECT * FROM holidays WHERE day = '{day}' AND year = '{year}'"
        query = QSqlQuery(r_query, QSqlDatabase().database(self.db_name))
        if not query.exec():
            print("Error executing query:", query.lastError().text())
            return
        if query.next():
            existing_id = int(query.value(0))
            if id ==-1:
                self.holidayEntryDuplicate.emit(existing_id)
                return
            elif id >= 0 and existing_id != id:
                self.holidayEntryDuplicate.emit(existing_id)
                return
        if id >=0:
            update_query = f"UPDATE holidays SET day = '{day}', hours = '{hours}', year = '{year}' WHERE id = {id}"
            query = QSqlQuery(update_query, QSqlDatabase().database(self.db_name))
            self.holidayEntrySaved.emit(query.exec())
        elif id == -1:
            insert_query = f"INSERT INTO holidays (day, hours, year) VALUES ('{day}', '{hours}', '{year}')"
            query = QSqlQuery(QSqlDatabase().database(self.db_name))
            if not query.exec(insert_query):
                print("Error executing query:", query.lastError().text())
            else:
                self.holidayEntrySaved.emit(True)

            r_query = f"SELECT id FROM holidays WHERE day = '{day}' AND year = '{year}'"
            query = QSqlQuery(r_query, QSqlDatabase().database(self.db_name))
            if not query.exec():
                print("Error executing query:", query.lastError().text())
                return
            if query.next():
                id = int(query.value(0))
                self.holidayEntryNew.emit(id)
    @QtCore.Slot(str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str)
    def save_metadata(self, company_name, company_street, company_zip, company_city, company_email, company_phone, employee_name, employee_street, employee_zip, employee_city, employee_id, employee_email, employee_phone, employee_holiday_entitlement, employee_weekly_hours, employee_daily_hours):
        del_query = "DELETE FROM meta"
        r_query = f"""INSERT INTO meta (company_name, company_street, company_city, company_zip, company_email, company_phone, employee_name, employee_street, employee_city, employee_zip, employee_email, employee_phone, employee_id, employee_holiday_entitlement, employee_weekly_hours, employee_daily_hours)
                   VALUES ('{company_name}', '{company_street}', '{company_city}', '{company_zip}', '{company_email}', '{company_phone}', '{employee_name}', '{employee_street}', '{employee_city}', '{employee_zip}', '{employee_email}', '{employee_phone}', '{employee_id}', '{employee_holiday_entitlement}', '{employee_weekly_hours}', '{employee_daily_hours}');"""
        connection = QSqlDatabase().database(self.db_name)
        query = QSqlQuery(connection)
        query.prepare(del_query)
        if not query.exec():
            print("Error while deleting metadata:", query.lastError().text())
        query.prepare(r_query)
        if not query.exec():
            print("Error while saving metadata:", query.lastError().text())
        else:
            print("Metadata saved successfully")

    @QtCore.Slot(int)
    def selectHolidayEntry(self, id):
        r_query = f"SELECT * FROM holidays WHERE id = {id}"
        query = QSqlQuery(r_query, QSqlDatabase().database(self.db_name))
        if not query.exec():
            print("Error executing query:", query.lastError().text())
            return
        while query.next():
            year = query.value(1)
            day = query.value(2)
            hours = query.value(3)
            self.holidayEntry.emit(id, day, hours, str(year))
            print(f"selectHolidayEntry: {id = }, {day = }, {hours = }, {year = }")

    @QtCore.Slot(int)
    def selectPublicHolidayEntry(self, id):
        r_query = f"SELECT * FROM public_holidays WHERE id = {id}"
        query = QSqlQuery(r_query, QSqlDatabase().database(self.db_name))
        if not query.exec():
            print("Error executing query:", query.lastError().text())
            return
        while query.next():
            day = query.value(2)
            description = query.value(3)
            hours = query.value(4)
            self.publicHolidayEntry.emit(id, day, description, hours, self.year)

    @QtCore.Slot(int)
    def selectSickdayEntry(self, id):
        r_query = f"SELECT * FROM sickdays WHERE id = {id}"
        query = QSqlQuery(r_query, QSqlDatabase().database(self.db_name))
        if not query.exec():
            print("Error executing query:", query.lastError().text())
            return
        while query.next():
            day = query.value(2)
            hours = query.value(3)
            self.sickdayEntry.emit(id, day, hours, self.year)

    @QtCore.Slot(str)
    def updateEntryQuery(self, topic: str):
        if topic == "":
            self.entryQueryChanged.emit('SELECT * FROM timecapturing ORDER BY year DESC, date', self.db_name)
            self.topicQueryChanged.emit('SELECT * FROM topics ORDER BY topic', self.db_name)
            self.holidayQueryChanged.emit('SELECT * FROM holidays ORDER BY day', self.db_name)
            self.publicHolidayQueryChanged.emit('SELECT * FROM public_holidays ORDER BY day', self.db_name)
            self.sickdayQueryChanged.emit('SELECT * FROM sickdays ORDER BY day', self.db_name)
            self.topicStandardQuery.emit(True)
        else:
            r_query = f"SELECT * FROM timecapturing WHERE topic = '{topic}'"
            # print(f"updateEntryQuery: {r_query}")
            self.entryQueryChanged.emit(r_query, self.db_name)

    @QtCore.Slot()
    def updateHolidayQuery(self):
        self.holidayQueryChanged.emit(f"SELECT * FROM holidays WHERE year = {self.year}", self.db_name)


