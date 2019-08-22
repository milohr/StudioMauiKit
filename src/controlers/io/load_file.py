# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)
from PySide2.QtCore import QObject, Slot
from PySide2.QtCore import QSettings
import threading
import queue
from src.controlers.util import read_raw


class LoadFile(QObject):
    """
    Upload and reads the raw signals
    """
    
    def __init__(self):
        QObject.__init__(self)
        self.list_path = []
        self.list_value_path = []
        self.project_name = ""
    
    def finished(self):
        print('Load and raw signal finished')
    
    @Slot(str)
    def set_project_name(self, name):
        from src.controlers.util import extract_name
        self.project_name = extract_name(name)
        # print(f'\033[1;36;40m SET PROJECT NAME: {self.project_name} \033[0m \n')
    
    @Slot(str)
    def read(self, path):
        que = queue.Queue()
        self.list_path = path.split(',')
        thread = threading.Thread(target = lambda q, arg1: q.put(read_raw(arg1)), args = (que, self.list_path)) #Necesito enviar el nombre del proyecto para guardar los valores
        thread.start()
        #thread.join()
        self.list_value_path = que.get() # Tiene es que agregar al final, no resetear
        print(f'\033[1;36;40m Value path: {self.list_value_path} \033[0m \n')
        # thread.join()
        # h = threading.Thread(target = read_raw, args = (path, ))
        # h.start()
        # h.join()
    
    @Slot(str)
    def assign_project(self, project):
        self.project_name = project
        settings = QSettings("Nebula", self.project_name)
        settings.beginGroup("SignalFiles")
        if self.list_path.__len__():
            settings.setValue("Path", self.list_path)
        else:
            settings.setValue("Path", "None")
        settings.endGroup()
    
    @Slot(str)
    def update_path(self, signal_name):
        from PySide2.QtCore import QDateTime
        
        settings = QSettings("Nebula", self.project_name)
        
        settings.beginGroup("Project")
        settings.setValue("LastEdit", QDateTime.currentDateTime().toString())
        settings.endGroup()
        
        settings.beginGroup("SignalFiles")
        before_list_path = settings.value("Path")
        before_list_path = before_list_path.split(',')
        print(f'Before list : {settings.fileName(), self.project_name, signal_name, before_list_path}')
        before_list_path.extend(self.list_path)
        print(f'\033[1;36;40m Before list path: {before_list_path} \033[0m \n')
        self.list_path = list(dict.fromkeys(before_list_path))  # Removes the repeated path names
        if 'None' in self.list_path:
            self.list_path.remove('None')
        actual_list_path = ','.join(self.list_path)
        print(f'\033[1;36;40m After list path: {actual_list_path} \033[0m \n')
        settings.setValue("Path", actual_list_path)
        settings.endGroup()
        del before_list_path, actual_list_path
    
    def update_value_path(self, value_path):
        self.list_value_path = value_path
