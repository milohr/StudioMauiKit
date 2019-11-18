# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)
from PySide2.QtCore import QObject, Slot
from PySide2.QtCore import QSettings
from PySide2.QtCore import QUrl
from PySide2.QtCore import QFileInfo
import os
from src.controlers.util import extract_name


class LoadProject(QObject):
    
    def __init__(self):
        QObject.__init__(self)
        self.name_project = ""
        self.project_to_load = ""
        self.path = ""
        self.settings = QSettings("Nebula")
        self.signal_path = []
        self.signal_value_path = []
    
    @Slot(str, result = 'QString')
    def get_name_project(self, *args):
        return self.name_project
    
    @Slot(str, result = 'QString')
    def create(self, name_project):
        """
        
        :param name_project: Name of the project
        :return: path of the settings file
        """
        from PySide2.QtCore import QDateTime
        self.name_project = name_project
        #print("from python " + self.name_project)
        self.settings = QSettings("Nebula", self.name_project)
        
        self.settings.beginGroup("Project")
        self.settings.setValue("Path", os.path.join(os.environ['HOME'], '.config/Nebula', self.name_project + '.conf'))
        self.settings.setValue("Name", self.name_project)
        self.settings.setValue("Date", QDateTime.currentDateTime().toString())
        self.settings.setValue("LastEdit", QDateTime.currentDateTime().toString())
        self.settings.endGroup()
        
        self.settings.beginGroup("SignalFiles")
        self.settings.setValue("Path", "None")  # Paths of the signals
        self.settings.setValue("ValuePath", "None")  # Value paths of the signals -numpy file
        self.settings.endGroup()

        self.settings.beginGroup("Info")
        self.settings.endGroup()
        
        print(self.settings.fileName())
        
        return self.settings.fileName()
    
    @Slot(str, result='QString')
    def settings_dir(self, past_path):
        return self.settings.fileName()

    @Slot(str, result='QString')
    def load(self, project):
        self.project_to_load = QUrl(project).toLocalFile()
        print(f'Project path loaded: {self.project_to_load}')
        self.name_project = extract_name(self.project_to_load)
        print(f'Project Name loaded: {self.name_project} and the other'
              f' way is: {QFileInfo(self.project_to_load).fileName()}')
        self.settings = QSettings("Nebula", self.name_project)
        self.settings.beginGroup("Project")
        self.path = self.settings.value("Path")
        self.name_project = self.settings.value("Name")
        self.settings.endGroup()
        self.settings.beginGroup("SignalFiles")
        self.signal_path = self.settings.value("Path")
        self.signal_value_path = self.settings.value("ValuePath")
        self.settings.endGroup()
        print(f'Organization name: {self.settings.organizationName(), self.settings.fileName()}')
        self.signal_path = self.signal_path.replace('None,', '')
        print(f'Loading signal files: {self.signal_path} type {type(self.signal_path)}')
        
        return self.signal_path
        
        

        
        
        
        
        
        
        
        
    