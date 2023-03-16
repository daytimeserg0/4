import sys
import psycopg2
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox, QTableWidgetItem, QPushButton, QMessageBox )


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Shedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_monday_tab()
        self._create_tuesday_tab()
        self._create_wednesday_tab()


    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="lab_8",
                                         user="postgres",
                                         password="A123a123s",
                                         host="localhost",
                                         port="5432")
        self.cursor = self.conn.cursor()


    def _create_monday_tab(self):
        self.monday_tab = QWidget()
        self.tabs.addTab(self.monday_tab, "Monday")

        self.monday_gbox = QGroupBox("Monday")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.monday_gbox)

        self._create_monday_table()

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.monday_tab.setLayout(self.svbox)


    def _create_tuesday_tab(self):
        self.tuesday_tab = QWidget()
        self.tabs.addTab(self.tuesday_tab, "Tuesady")

        self.tuesday_gbox = QGroupBox("Tuesday")

        self.tvbox = QVBoxLayout()
        self.thbox1 = QHBoxLayout()
        self.thbox2 = QHBoxLayout()

        self.tvbox.addLayout(self.thbox1)
        self.tvbox.addLayout(self.thbox2)

        self.thbox1.addWidget(self.tuesday_gbox)

        self._create_tuesday_table()

        self.update_shedule_button2 = QPushButton("Update")
        self.thbox2.addWidget(self.update_shedule_button2)
        self.update_shedule_button2.clicked.connect(self._update_shedule2)

        self.tuesday_tab.setLayout(self.tvbox)


    def _create_wednesday_tab(self):
        self.wednesday_tab = QWidget()
        self.tabs.addTab(self.wednesday_tab, "Wednesday")

        self.wednesday_gbox = QGroupBox("Wednesday")

        self.wvbox = QVBoxLayout()
        self.whbox1 = QHBoxLayout()
        self.whbox2 = QHBoxLayout()

        self.wvbox.addLayout(self.whbox1)
        self.wvbox.addLayout(self.whbox2)

        self.whbox1.addWidget(self.wednesday_gbox)

        self._create_wednesday_table()

        self.update_shedule_button3 = QPushButton("Update")
        self.whbox2.addWidget(self.update_shedule_button3)
        self.update_shedule_button3.clicked.connect(self._update_shedule3)

        self.wednesday_tab.setLayout(self.wvbox)

    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table.setColumnCount(5)
        self.monday_table.setHorizontalHeaderLabels(["Time", "Subject", "Auditorium", "", ""])

        self._update_monday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)


    def _create_tuesday_table(self):
        self.tuesday_table = QTableWidget()
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.tuesday_table.setColumnCount(5)
        self.tuesday_table.setHorizontalHeaderLabels(["Time", "Subject", "Auditorium", "", ""])

        self._update_tuesday_table()

        self.mvbox1 = QVBoxLayout()
        self.mvbox1.addWidget(self.tuesday_table)
        self.tuesday_gbox.setLayout(self.mvbox1)


    def _create_wednesday_table(self):
        self.wednesday_table = QTableWidget()
        self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.wednesday_table.setColumnCount(5)
        self.wednesday_table.setHorizontalHeaderLabels(["Time", "Subject", "Auditorium", "", ""])

        self._update_wednesday_table()

        self.mvbox2 = QVBoxLayout()
        self.mvbox2.addWidget(self.wednesday_table)
        self.wednesday_gbox.setLayout(self.mvbox2)

    def _update_monday_table(self):
        self.cursor.execute("SELECT * FROM timetable ORDER BY id")
        records = list(self.cursor.fetchall())

        self.monday_table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)
            stroke_updateButton = QPushButton("change")
            stroke_deleteButton = QPushButton("delete")

            self.monday_table.setItem(i, 0, QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 2, QTableWidgetItem(str(r[4])))
            self.monday_table.setCellWidget(i, 3, stroke_updateButton)
            self.monday_table.setCellWidget(i, 4, stroke_deleteButton)

            d='Monday'
            stroke_updateButton.clicked.connect(lambda ch, num=i: self._change_day_from_monday(num, d))
            stroke_deleteButton.clicked.connect(lambda ch, num=i: self._delete_day_from_monday(num, d))
            stroke_deleteButton.clicked.connect(self._update_shedule)

        self.monday_table.resizeRowsToContents()


    def _update_tuesday_table(self):
        self.cursor.execute("SELECT * FROM timetable_2 ORDER BY id")
        records = list(self.cursor.fetchall())

        self.tuesday_table.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            stroke_updateButton2 = QPushButton("change")
            stroke_deleteButton2 = QPushButton("delete")

            self.tuesday_table.setItem(i, 0, QTableWidgetItem(str(r[2])))
            self.tuesday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.tuesday_table.setItem(i, 2, QTableWidgetItem(str(r[4])))
            self.tuesday_table.setCellWidget(i, 3, stroke_updateButton2)
            self.tuesday_table.setCellWidget(i, 4, stroke_deleteButton2)

            d='Tuesday'
            stroke_updateButton2.clicked.connect(lambda ch, num=i: self._change_day_from_tuesday(num, d))
            stroke_deleteButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_tuesday(num, d))
            stroke_deleteButton2.clicked.connect(self._update_shedule2)

        self.tuesday_table.resizeRowsToContents()


    def _update_wednesday_table(self):
        self.cursor.execute("SELECT * FROM timetable_3 ORDER BY id")
        records = list(self.cursor.fetchall())

        self.wednesday_table.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            stroke_updateButton3 = QPushButton("change")
            stroke_deleteButton3 = QPushButton("delete")

            self.wednesday_table.setItem(i, 0, QTableWidgetItem(str(r[2])))
            self.wednesday_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.wednesday_table.setItem(i, 2, QTableWidgetItem(str(r[4])))
            self.wednesday_table.setCellWidget(i, 3, stroke_updateButton3)
            self.wednesday_table.setCellWidget(i, 4, stroke_deleteButton3)

            d='Wednesday'
            stroke_updateButton3.clicked.connect(lambda ch, num=i: self._change_day_from_wednesday(num, d))
            stroke_deleteButton3.clicked.connect(lambda ch, num=i: self._delete_day_from_wednesday(num, d))
            stroke_deleteButton3.clicked.connect(self._update_shedule3)

        self.wednesday_table.resizeRowsToContents()


    def _delete_day_from_monday(self, rowNum, day):
        row = list()
        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f'UPDATE timetable SET location = \'\', subject = \'\' WHERE start_time = \'{row[0]}\'')
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Нельзя изменить время")
            self._update_shedule()


    def _delete_day_from_tuesday(self, rowNum, day):
        row = list()
        for i in range(self.tuesday_table.columnCount()):
            try:
                row.append(self.tuesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f'UPDATE timetable_2 SET location = \'\', subject = \'\' WHERE start_time = \'{row[0]}\'')
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Нельзя изменить время")
            self._update_shedule2()


    def _delete_day_from_wednesday(self, rowNum, day):
        row = list()
        for i in range(self.wednesday_table.columnCount()):
            try:
                row.append(self.wednesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f'UPDATE timetable SET location = \'\', subject = \'\' WHERE start_time = \'{row[0]}\'')
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Нельзя изменить время")
            self._update_shedule3()


    def _change_day_from_monday(self, rowNum, day):
        row = list()
        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f'UPDATE timetable SET location = \'{row[2]}\', subject = \'{row[1]}\' WHERE start_time = \'{row[0]}\'')
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Нельзя изменить время")
            self._update_shedule()


    def _change_day_from_tuesday(self, rowNum, day):
        row = list()
        for i in range(self.tuesday_table.columnCount()):
            try:
                row.append(self.tuesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f'UPDATE timetable_2 SET location = \'{row[2]}\', subject = \'{row[1]}\' WHERE start_time = \'{row[0]}\'')
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Нельзя изменить время")
            self._update_shedule2()

    def _change_day_from_wednesday(self, rowNum, day):
        row = list()
        for i in range(self.wednesday_table.columnCount()):
            try:
                row.append(self.wednesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f'UPDATE timetable_3 SET location = \'{row[2]}\', subject = \'{row[1]}\' WHERE start_time = \'{row[0]}\'')
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Нельзя изменить время")
            self._update_shedule3()

    def _update_shedule(self):
        self._update_monday_table()

    def _update_shedule2(self):
        self._update_tuesday_table()

    def _update_shedule3(self):
        self._update_wednesday_table()

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())