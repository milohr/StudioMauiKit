# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)
import subprocess

from PySide2.QtCore import QObject, Slot
from PySide2.QtCore import QSettings
from PySide2.QtCore import QDateTime

from src.controlers.thread_with_return import ThreadWithReturn
from src.controlers.util import read_raw, read_info


class LoadFile(QObject):
    """
    Upload and reads the raw signals
    """
    
    def __init__(self):
        QObject.__init__(self)
        self.list_path = list()
        self.list_value_path = list()
        self.project_name = ""
        self.info = list()
        self.sfreq = list()
    
    def finished(self):
        print('Load and raw signal finished')
    
    @Slot(str)
    def set_project_name(self, name):
        from src.controlers.util import extract_name
        self.project_name = extract_name(name)
        # print(f'\033[1;36;40m SET PROJECT NAME: {self.project_name} \033[0m \n')
    
    @Slot(str)
    def read(self, path):
        #que = queue.Queue()
        self.list_path = path.split(',')
        thread = ThreadWithReturn(target = read_raw, args = (self.list_path,))
        #thread = threading.Thread(target = lambda q, arg1: q.put(read_raw(arg1)), args = (que, self.list_path)) #Necesito enviar el nombre del proyecto para guardar los valores
        thread.start()
        #self.list_value_path.extend(que.get())
        self.list_value_path.extend(thread.join())
        self.list_value_path = list(dict.fromkeys(self.list_value_path))
        print(f'\033[1;36;40m Value path: {self.list_value_path} \033[0m \n')
        self.info, self.sfreq = read_info(self.list_path)
        self.update_value_path(self.list_value_path)
        
    
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

        self.info, self.sfreq = read_info(self.list_path)
        settings.beginGroup("Info")
        settings.beginWriteArray("sfreq")
        for i in range(len(self.sfreq)):
            settings.setArrayIndex(i)
            settings.setValue("sfreq", self.sfreq[i])
        settings.endArray()
        settings.beginWriteArray("SubjectInfo")
        for i in range(len(self.info)):
            settings.setArrayIndex(i)
            for key, value in self.info[i].items():
                settings.setValue(key, str(value))
        settings.endArray()
        settings.endGroup()
        del before_list_path, actual_list_path
    
    def update_value_path(self, value_path):
        settings = QSettings("Nebula", self.project_name)

        settings.beginGroup("Project")
        settings.setValue("LastEdit", QDateTime.currentDateTime().toString())
        settings.endGroup()
        
        settings.beginGroup("SignalFiles")
        before_path = settings.value("ValuePath")
        before_path = before_path.split(',')
        before_path.extend(value_path)
        self.list_value_path = list(dict.fromkeys(before_path))
        if 'None' in self.list_path:
            self.list_value_path.remove('None')
        actual_path = ','.join(self.list_value_path)
        settings.setValue("ValuePath", actual_path)  # Tengo que leer primero qeu hay aqui y luego actualizar
        settings.endGroup()
        del actual_path, before_path
    
    @Slot(str)
    def raw_plot(self, path):
        try:
            new_gui = subprocess.Popen(["python",
                                        "/home/kevrodz/Documents/Nebula/src/controlers/multiple_plot.py",
                                        self.list_value_path[1] if self.list_value_path[0] == 'None' else self.list_value_path[0]])
        except:
            print('Can not plot signal')
        # manager = Manager()
        # data = manager.list()
        # p = Process(target = f, args = ('bob',))
        # p.start()
        # input("Type any key to quit.")
        # print("Waiting for graph window process to join...")
        # p.join()
        # print("Process joined successfully. C YA !")

        #sys.exit(app.exec_())