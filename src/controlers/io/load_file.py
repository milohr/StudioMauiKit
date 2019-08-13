# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)
from PySide2.QtCore import QObject, Slot
from mne.io import read_raw_cnt
import numpy as np
import os
import threading
from PySide2.QtCore import QSettings


def read_raw(path):
    """

    :rtype: object
    :param path: Path of the files that contain the signal
    :return:
    """
    list_path = path.split(',')
    print(f'Signal path list: {list_path}')
    try:
        # Read raw signal
        raw = {k: read_raw_cnt(k, montage = None, preload = True,
                               stim_channel = False, verbose = None) for k in list_path}
        raw2np = {}
        # Print the multiples upload signals
        for signal in raw:
            print(f'\033[1;32;40m {raw[signal]} \033[0m \n')
            print(f'\033[1;33;40m {raw[signal].info} \033[0m \n')
        b = []
        # Values in a numpy array in a dict way
        raw2np = {i: np.squeeze(raw[i].get_data()) for i in raw}
        for keys in raw2np.keys():
            print(f'\033[1;32;40m Key: {keys} \033[0m \n ')
            print(f'\033[1;35;40m Values: {raw2np[keys]} \033[0m \n')
            np.save(os.path.join(os.getcwd(), str(keys) + '.npy'), raw2np[keys])
            b.append(np.load(os.path.join(os.getcwd(), str(
                keys) + '.npy')))  # List with the values, each position is a differente file
        # print(b.__len__(), b[0].shape, b[1].shape)
    except IOError:
        print('An error occurred trying to read the file.')
    except ImportError:
        print('No file found.')
    except:
        print('Cant read file')
    finally:
        print('Upload signal(s) correctly')
        # callback()


class LoadFile(QObject):
    """
    Upload and reads the raw signals
    """
    
    def __init__(self):
        QObject.__init__(self)
        self.list_path = []
        self.project_name = ""
    
    def finished(self):
        print('Load and raw signal finished')
    
    @Slot(str)
    def set_project_name(self, name):
        from src.controlers.util import extract_name
        self.project_name = extract_name(name)
        #print(f'\033[1;36;40m SET PROJECT NAME: {self.project_name} \033[0m \n')
    
    @Slot(str)
    def read(self, path):
        self.list_path = path
        thread = threading.Thread(target = read_raw, args = (self.list_path,))
        thread.start()
        # thread.join()
        # h = threading.Thread(target = read_raw, args = (path, ))
        # h.start()
        # h.join()
    
    @Slot(str)
    def assign_project(self, project):
        self.project_name = project
        settings = QSettings("Nebula", self.project_name)
        settings.beginGroup("SignalFiles")
        settings.setValue("Path", self.list_path)
        settings.endGroup()
    
    @Slot(str)
    def update_path(self, signal_name):
        #from src.controlers.util import extract_name
        #self.project_name = extract_name(signal_name)
        settings = QSettings("Nebula", self.project_name)
        settings.beginGroup("SignalFiles")
        before_list_path = settings.value("Path")
        print(
            f'befores list : {settings.fileName(), self.project_name, signal_name}'
        )
        actual_list_path = self.list_path
        entire_path = lambda x, y: x + ', ' + y
        self.list_path = entire_path(before_list_path, actual_list_path)
        print(f'\033[1;36;40m AQUIIIIIII: {self.list_path} \033[0m \n')
        settings.setValue("Path", self.list_path)
        del before_list_path, actual_list_path
        # if not settings.value("Path") or not settings.value("Path").strip():
        #     settings.setValue("Path", self.list_path)
        # else:
        #     before_list_path = settings.value("Path")
        #     actual_list_path = self.list_path
        #     entire_path = lambda x, y: x + ', ' + y
        #     self.list_path = entire_path(before_list_path, actual_list_path)
        #     print(f'\033[1;36;40m AQUIIIIIII: {self.list_path} \033[0m \n')
        #     settings.setValue("Path", self.list_path)
        #     del before_list_path, actual_list_path
        settings.endGroup()
    
    '''
    @Slot(str)
    def read_raw2(self, path):
        """
        
        :param path: Path of the files that contain the signal
        :return:
        """
        
        self.list_path = path.split(',')
        print(f'Signal path list: {self.list_path}')
        try:
            # Read raw signal
            raw = {k: read_raw_cnt(k, montage = None, preload=True,
                                   stim_channel=False, verbose=None) for k in self.list_path}
            raw2np = {}
            # Print the multiples upload signals
            for signal in raw:
                print(f'\033[1;32;40m {raw[signal]} \033[0m \n')
                print(f'\033[1;33;40m {raw[signal].info} \033[0m \n')
            b = []
            j = 0
            # Values in a numpy array in a dict way
            raw2np = {i: np.squeeze(raw[i].get_data()) for i in raw}
            for keys in raw2np.keys():
                print(f'\033[1;32;40m Key: {keys} \033[0m \n ')
                print(f'\033[1;35;40m Values: {raw2np[keys]} \033[0m \n')
                np.save(os.path.join(os.getcwd(), str(keys)+'.npy'), raw2np[keys])
                b.append(np.load(os.path.join(os.getcwd(), str(keys)+'.npy'))) # List with the values, each position is a differente file
            #print(b.__len__(), b[0].shape, b[1].shape)
        except IOError:
            print('An error occurred trying to read the file.')
        except ImportError:
            print('No file found.')
        except:
            print('Cant read file')
        finally:
            print('Upload signal(s) correctly')
     '''
