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

        self._create_week_tab()
        self._create_teacher_tab()
        self._create_subject_tab()
        self._create_schedule_tab()


    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="schedule_for_lab_8",
                                         user="postgres",
                                         password="A123a123s",
                                         host="localhost",
                                         port="5432")
        self.cursor = self.conn.cursor()


    def _create_week_tab(self):
        self.week_tab = QWidget()
        self.tabs.addTab(self.week_tab, "Week")

        self.week_gbox = QGroupBox("Week")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.week_gbox)

        self._create_week_table()

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.week_tab.setLayout(self.svbox)


    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Teachers")

        self.teacher_gbox = QGroupBox("Teachers")

        self.tvbox = QVBoxLayout()
        self.thbox1 = QHBoxLayout()
        self.thbox2 = QHBoxLayout()

        self.tvbox.addLayout(self.thbox1)
        self.tvbox.addLayout(self.thbox2)

        self.thbox1.addWidget(self.teacher_gbox)

        self._create_teacher_table()

        self.add_shedule_button = QPushButton('Add')
        self.update_shedule_button2 = QPushButton("Update")
        self.thbox2.addWidget(self.update_shedule_button2)
        self.thbox2.addWidget(self.add_shedule_button)
        self.add_shedule_button.clicked.connect(self._add_shedule)
        self.update_shedule_button2.clicked.connect(self._update_shedule2)

        self.teacher_tab.setLayout(self.tvbox)


    def _create_subject_tab(self):
        self.subject_tab = QWidget()
        self.tabs.addTab(self.subject_tab, "Subjects")

        self.subject_gbox = QGroupBox("Subjects")

        self.wvbox = QVBoxLayout()
        self.whbox1 = QHBoxLayout()
        self.whbox2 = QHBoxLayout()

        self.wvbox.addLayout(self.whbox1)
        self.wvbox.addLayout(self.whbox2)

        self.whbox1.addWidget(self.subject_gbox)

        self._create_subject_table()

        self.add_shedule_button2 = QPushButton("Add")
        self.update_shedule_button3 = QPushButton("Update")
        self.whbox2.addWidget(self.update_shedule_button3)
        self.whbox2.addWidget(self.add_shedule_button2)
        self.update_shedule_button3.clicked.connect(self._update_shedule3)
        self.add_shedule_button2.clicked.connect(self._add_shedule2)

        self.subject_tab.setLayout(self.wvbox)


    def _create_schedule_tab(self):
        self.schedule_tab = QWidget()
        self.tabs.addTab(self.schedule_tab, "Full schedule")

        self.schedule_gbox = QGroupBox("Full schedule")

        self.fvbox = QVBoxLayout()
        self.fhbox1 = QHBoxLayout()
        self.fhbox2 = QHBoxLayout()

        self.fvbox.addLayout(self.fhbox1)
        self.fvbox.addLayout(self.fhbox2)

        self.fhbox1.addWidget(self.schedule_gbox)

        self._create_schedule_table()
        self.schedule_tab.setLayout(self.fvbox)

    def _create_week_table(self):
        self.week_table = QTableWidget()
        self.week_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.week_table.setColumnCount(6)
        self.week_table.setHorizontalHeaderLabels(["Day", "Time", "Subject", "Auditorium", "", ""])

        self._update_week_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.week_table)
        self.week_gbox.setLayout(self.mvbox)


    def _create_teacher_table(self):
        self.teacher_table = QTableWidget()
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teacher_table.setColumnCount(5)
        self.teacher_table.setHorizontalHeaderLabels(["Id", "Teacher", "Subject", "", ""])

        self._update_teacher_table()

        self.mvbox1 = QVBoxLayout()
        self.mvbox1.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.mvbox1)


    def _create_subject_table(self):
        self.subject_table = QTableWidget()
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subject_table.setColumnCount(4)
        self.subject_table.setHorizontalHeaderLabels(["Id", "Subject", "", ""])

        self._update_subject_table()

        self.mvbox2 = QVBoxLayout()
        self.mvbox2.addWidget(self.subject_table)
        self.subject_gbox.setLayout(self.mvbox2)

    def _create_schedule_table(self):
        self.schedule_table = QTableWidget()
        self.schedule_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.schedule_table.setColumnCount(5)
        self.schedule_table.setHorizontalHeaderLabels(["Day", "Time", "Subject","Teacher", "Auditorium"])

        self._update_schedule_table()

        self.fvbox = QVBoxLayout()
        self.fvbox.addWidget(self.schedule_table)
        self.schedule_gbox.setLayout(self.fvbox)

    def _update_week_table(self):
        self.cursor.execute("SELECT * FROM firs_week ORDER BY id")
        records = list(self.cursor.fetchall())

        self.week_table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)
            stroke_updateButton = QPushButton("change")
            stroke_deleteButton = QPushButton("delete")

            self.week_table.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.week_table.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.week_table.setItem(i, 2, QTableWidgetItem(str(r[3])))
            self.week_table.setItem(i, 3, QTableWidgetItem(str(r[4])))
            self.week_table.setCellWidget(i, 4, stroke_updateButton)
            self.week_table.setCellWidget(i, 5, stroke_deleteButton)

            d='Monday'
            stroke_updateButton.clicked.connect(lambda ch, num=i: self._change_day_from_week(num, d))
            stroke_deleteButton.clicked.connect(lambda ch, num=i: self._delete_day_from_week(num, d))
            stroke_deleteButton.clicked.connect(self._update_shedule)

        self.week_table.resizeRowsToContents()


    def _update_teacher_table(self):
        self.cursor.execute("SELECT * FROM teacher ORDER BY id")
        records = list(self.cursor.fetchall())

        self.teacher_table.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            stroke_updateButton2 = QPushButton("change")
            stroke_deleteButton2 = QPushButton("delete")

            self.teacher_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.teacher_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.teacher_table.setCellWidget(i, 3, stroke_updateButton2)
            self.teacher_table.setCellWidget(i, 4, stroke_deleteButton2)

            d='teacher'
            stroke_updateButton2.clicked.connect(lambda ch, num=i: self._change_day_from_teacher(num, d))
            stroke_deleteButton2.clicked.connect(lambda ch, num=i: self._delete_day_from_teacher(num, d))
            stroke_deleteButton2.clicked.connect(self._update_shedule2)

        self.teacher_table.resizeRowsToContents()


    def _update_subject_table(self):
        self.cursor.execute("SELECT * FROM subject ORDER BY id")
        records = list(self.cursor.fetchall())

        self.subject_table.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            stroke_deleteButton3 = QPushButton("delete")
            stroke_changeButton3 = QPushButton("change")

            self.subject_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.subject_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.subject_table.setCellWidget(i, 2, stroke_changeButton3)
            self.subject_table.setCellWidget(i, 3, stroke_deleteButton3)

            d='subject'
            stroke_deleteButton3.clicked.connect(lambda ch, num=i: self._delete_day_from_subject(num, d))
            stroke_changeButton3.clicked.connect(lambda ch, num=i: self._change_day_from_subject(num, d))
            stroke_deleteButton3.clicked.connect(self._update_shedule3)

        self.subject_table.resizeRowsToContents()

    def _update_schedule_table(self):
        self.cursor.execute('SELECT firs_week.day, firs_week.time, firs_week.subject, '
                            'teacher.name, firs_week.room FROM firs_week JOIN teacher ON firs_week.subject = teacher.subject ORDER BY firs_week.id;')
        records = list(self.cursor.fetchall())

        self.schedule_table.setRowCount(len(records))
        for i, r in enumerate(records):
            r = list(r)

            self.schedule_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.schedule_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.schedule_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.schedule_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            self.schedule_table.setItem(i, 4, QTableWidgetItem(str(r[4])))

        self.schedule_table.resizeRowsToContents()


    def _delete_day_from_week(self, rowNum, day):
        row = list()
        for i in range(self.week_table.columnCount()):
            try:
                row.append(self.week_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f'UPDATE firs_week SET room = \'\', subject = \'\' WHERE day = \'{row[0]}\' AND time = \'{row[1]}\'')
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Нельзя изменить время")
            self._update_shedule()


    def _delete_day_from_teacher(self, rowNum, day):
        row = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f'DELETE FROM teacher WHERE id = \'{row[0]}\'')
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Нельзя изменить id")
            self._update_shedule2()


    def _delete_day_from_subject(self, rowNum, day):
        row = list()
        for i in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f'DELETE FROM subject WHERE id = \'{row[0]}\'')
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Нельзя изменить время")
            self._update_shedule3()


    def _change_day_from_week(self, rowNum, day):
        row = list()
        for i in range(self.week_table.columnCount()):
            try:
                row.append(self.week_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f'UPDATE firs_week SET room = \'{row[3]}\', subject = \'{row[2]}\' WHERE day = \'{row[0]}\' AND time = \'{row[1]}\'')
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Проверьте не меняли ли вы время или день/, или же вы ввели предмет, которого нет в списке")
        self._update_shedule()


    def _change_day_from_teacher(self, rowNum, day):
        row = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute(f'UPDATE teacher SET name = \'{row[1]}\', subject = \'{row[2]}\' WHERE id = \'{row[0]}\'')
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Проверьте не изменили ли вы id ,и есть ли ваш предмет в списке")
        self._update_shedule2()

    def _change_day_from_subject(self, rowNum, day):
        row = list()
        for i in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, i).text())
                print(row)
            except:
                row.append(None)
        try:
            self.cursor.execute(f'UPDATE subject SET name = \'{row[1]}\' WHERE id = {row[0]};')
            self.conn.commit()
            print(1)
        except:
            QMessageBox.about(self, "Error", "Либо предмет с таким именем уже существует, либо этот предмет нельзя изменить т.к. другие таблицы опираются на него")
        self._update_shedule3()

    def _update_shedule(self):
        self._update_week_table()
        self._update_schedule_table()

    def _update_shedule2(self):
        self._update_teacher_table()
        self._update_schedule_table()

    def _update_shedule3(self):
        self._update_subject_table()
        self._update_schedule_table()

    def _add_shedule(self):
        self.cursor.execute('INSERT INTO teacher (name, subject) VALUES (\'\', \'\');')
        self.conn.commit()
        self._update_shedule2()

    def _add_shedule2(self):
        try:
            self.cursor.execute('INSERT INTO subject (name) VALUES (\'New subject\');')
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Сначала измените новый предмет")
        self._update_shedule3()

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())