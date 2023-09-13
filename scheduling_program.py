from PyQt5 import QtWidgets, uic, QtCore
import sys
from sqlite3 import *

class Task:
    def __init__(self, name, duration, priority):
        #Used to create object instances of each class
        self.name = name
        self.duration = duration
        self.priority = priority
        

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = self.dataConversion(data)
        self.header_labels = ['Task ', 'Start Time', 'End Time']
        self._checked = [False for i in range(len(self._data))]
    
    def data(self, index, role):
        #Adds the data to the model and initially leaves each task unchecked
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        if role == QtCore.Qt.CheckStateRole:
            checked = self._checked[index.row()]
            if index.column() == 0:
                return QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked

    def setData(self, index, value, role):
        #Allows the user to check tasks if they have been completed
        if role == QtCore.Qt.CheckStateRole:
            checked = value == QtCore.Qt.Checked
            self._checked[index.row()] = checked
            return True
        
    def dataConversion(self, data):
        #Converts the data from being a list of objects to a 2D array that the table model can use
        new_data = []
        for i in range(len(data)):
            start_time = f"{(data[i].start_time // 60):02d}:{(data[i].start_time % 60):02d}"
            end_time = f"{(data[i].end_time // 60):02d}:{(data[i].end_time % 60):02d}"
            new_data.append([data[i].name, start_time, end_time])
        return new_data
            
    def rowCount(self, index):
        #Returns the number of rows
        return len(self._data)

    def columnCount(self, index):
        #returns the number of columns, if any
        try:
            return len(self._data[0])
        except:
            return 0
    
    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsUserCheckable
    
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        #Adds header labels to the model
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header_labels[section]
        return super().headerData(section, orientation, role)
    
def schedule_tasks(tasks, start_time, end_time, break_start, break_end):
    # Sort tasks based on priority and duration
    tasks.sort(key=lambda x: (x.priority, x.duration), reverse=True)

    current_time = start_time
    scheduled_tasks = []
    unscheduled_tasks = []

    for task in tasks:
        # Check if there is enough time for the task including breaks
        if current_time + task.duration <= end_time:
            task_start_time = current_time
            task_end_time = task_start_time + task.duration

            # Check if the task conflicts with the break time
            if task_start_time < break_start < task_end_time or task_start_time < break_end < task_end_time:
                # Task conflicts with the break, but we'll reschedule it after the break if possible
                task_start_time = max(task_end_time, break_end)
                task_end_time = task_start_time + task.duration

            # Assign start and end time to the task
            task.start_time = task_start_time
            task.end_time = task_end_time

            scheduled_tasks.append(task)
            current_time = task_end_time

        else:
            unscheduled_tasks.append(task)

    return scheduled_tasks, unscheduled_tasks


class Menu(QtWidgets.QMainWindow):
    def __init__(self):
        super(Menu, self).__init__() # Calls the inherited classes __init__ method
        uic.loadUi('main_menu.ui',self) #Loads the ui file
        
        #Handles the events of buttons being clicked
        self.add_task_button.clicked.connect(self.add_task_method)
        self.reset_button.clicked.connect(self.reset_method)
        self.save_settings_button.clicked.connect(self.save_settings_method)

        #Handles the event of a tab being changed
        self.tabWidget.currentChanged.connect(self.onChange)

        self.current_tasks = []
        self.start_time = 9 * 60
        self.end_time = 18 * 60
        self.break_start = 12 * 60
        self.break_end = 13 * 60

        #Current table model
        self.__current_model = None
        self.__unresolved_update = False

        self.scheduled_tasks = None
        self.unscheduled_tasks = None
        
        self.show()

    def add_task_method(self):
        #Adds a task entered by the user to the current list of tasks after validation
        try:
            task_name = self.task_name_input.text()
            task_duration = int(self.duration_input.text())

            priority = self.priority_slider.value()
            self.current_tasks.append(Task(task_name, task_duration, priority))
            if task_name == '' or task_duration == '':
                self.input_response_label.setText('Please do not leave any fields blank!')
            else:
                self.reset_method()
                self.input_response_label.setText('Task Added Successfully!')
                self.__unresolved_update = True
        except ValueError:
            self.input_response_label.setText('Please enter a task duration in minutes!')

    def reset_method(self):
        #Resets all the input fields for the add tasks section
        self.task_name_input.setText('')
        self.duration_input.setText('')
        self.priority_slider.setValue(1)
        self.input_response_label.setText('')

    def save_settings_method(self):
        #Saves the new start/end times and break time entered by the user
        start_input = self.day_start_input.time().toPyTime()
        end_input = self.day_end_input.time().toPyTime()
        brk_start_input = self.break_start_input.time().toPyTime()
        brk_end_input = self.break_end_input.time().toPyTime()

        self.start_time = start_input.hour * 60 + start_input.minute
        self.end_hour = end_input.hour * 60 + end_input.minute
        self.break_start_hour = brk_start_input.hour * 60 + brk_start_input.minute
        self.break_end_hour = brk_end_input.minute * 60 + brk_end_input.minute

        self.settings_save_response_label.setText('Your Settings Have Been Saved!')
        self.__unresolved_update = True
    
    def view_schedule_method(self):
        if self.__unresolved_update:
            #Updates to a new schedule if a new task has been added or settings are changed
            self.scheduled_tasks, self.unscheduled_tasks = schedule_tasks(self.current_tasks, self.start_time, self.end_time, self.break_start, self.break_end)
            
            #Updates the table showing tasks 
            self.task_table_view.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.task_table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.__current_model = TableModel(self.scheduled_tasks)
            self.task_table_view.setModel(self.__current_model)
            self.task_table_view.horizontalHeader().setVisible(True)

            #Displays any unscheduled tasks in a list underneath the table
            if self.unscheduled_tasks:
                unscheduled_tasks_text = "Unscheduled Tasks:\n"
                for task in self.unscheduled_tasks:
                    unscheduled_tasks_text += task.name + ", "
                self.unscheduled_label.setText(unscheduled_tasks_text[:-2])
            self.__unresolved_update = False
            
    #@pyqtSlot()  
    def onChange(self, index):
        #Calls a method based on what the current tab has been changed to
        if index == 0:
            self.reset_method()
        elif index == 1:
            self.view_schedule_method()

def main():
    #Initialises and displays window
    app = QtWidgets.QApplication(sys.argv)
    window = Menu()
    app.exec_()


main()