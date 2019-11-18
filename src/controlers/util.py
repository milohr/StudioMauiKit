# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)
from PySide2.QtCore import QSettings
from functools import wraps
import numpy as np
from multiprocessing.pool import ThreadPool


def extract_name(path):
    """
    Extract the name from a path
    :param path: Str, having in the end of the line the name to extract with the .conf format
    :return: name
    """
    import os
    head_tail = os.path.split(path)
    name = head_tail[1].replace(".conf", "")
    del head_tail
    return name


def update(path):
    return path


def read_info(path):
    from PySide2.QtCore import QUrl
    from mne.io import read_raw_cnt, read_raw_eeglab
    
    list_path = [QUrl(i).toLocalFile() for i in path]
    
    try:
        raw = {k: read_raw_cnt(k,
                               montage = None,
                               preload = True,
                               stim_channel = False,
                               verbose = None
                               ) if k.endswith("cnt"
                                               ) else read_raw_eeglab(k,
                                                                      montage = None,
                                                                      preload = True,
                                                                      stim_channel = False,
                                                                      verbose = None) for k in list_path}
        info = list()
        sfreq = list()
        for signal in raw:
            raw_info = raw[signal].info
            info.append(raw_info['subject_info'])
            sfreq.append(raw_info['sfreq'])
        del raw
        return info, sfreq
            
        
    except IOError:
        print('An error occurred trying to read the file.')
    except ImportError:
        print('No file found.')
    except:
        print('Cant read file')
    finally:
        print('Upload info correctly')
        

def read_raw(path):
    """

    :rtype: object
    :param path: Path of the files that contain the signal
    :return:
    """
    from PySide2.QtCore import QUrl
    from mne.io import read_raw_cnt, read_raw_eeglab
    import numpy as np
    import os
    
    # list_path = path.split(',')
    list_path = [QUrl(i).toLocalFile() for i in path]
    print(f'Signal path list: {list_path}')
    
    try:
        # Read raw signal
        raw = {k: read_raw_cnt(k,
                               montage = None,
                               preload = True,
                               stim_channel = False,
                               verbose = None
                               ) if k.endswith("cnt"
                                               ) else read_raw_eeglab(k,
                                                                      montage = None,
                                                                      preload = True,
                                                                      stim_channel = False,
                                                                      verbose = None
                                                                      ) for k in list_path}
        # raw = {k: read_raw_cnt(k, montage = None, preload = True,
        #                      stim_channel = False, verbose = None) for k in list_path}
        
        # Print the multiples upload signals
        for signal in raw:
            print(f'\033[1;32;40m {raw[signal]} \033[0m \n')
            print(f'\033[1;33;40m {raw[signal].info} \033[0m \n')
        b = []
        value_path = []
        # Values in a numpy array in a dict way
        raw2np = {i: np.squeeze(raw[i].get_data()) for i in raw}  # This contain the entire already uploaded data
        for keys in raw2np.keys():
            print(f'\033[1;32;40m Key: {keys} \033[0m \n ')
            print(f'\033[1;35;40m Values: {raw2np[keys]} \033[0m \n')
            np_path = str(keys).replace('.cnt' if str(keys).endswith('cnt') else '.set', '.npz')
            print('Path keys ', np_path)
            np.savez_compressed(np_path, raw2np[keys])
            # print(np.load(np_path))  # Organizar esto en otro hilo pero bien organizado para cargarlo despues
            value_path.append(os.path.join(os.getcwd(), np_path))
            b.append(np.load(np_path))  # List with the values, each position is a different file
        
        print(f'Value path: {value_path}')
        # Update in settings the value path
        
        print(os.getcwd() + "--" + str(keys))
        # print(b.__len__(), b[0].shape, b[1].shape)
        return value_path
    except IOError:
        print('An error occurred trying to read the file.')
    except ImportError:
        print('No file found.')
    except:
        print('Cant read file')
    finally:
        print('Upload signal(s) correctly')
        # callback()


def get_data_path(name_project):
    settings = QSettings("Nebula", name_project)
    settings.beginGroup("SignalFiles")
    signal_value_path = settings.value("ValuePath")
    settings.endGroup()
    try:
        print(signal_value_path)
        signal_value_path = signal_value_path.split(',')
        if 'None' in signal_value_path:
            signal_value_path.remove('None')
        print(f'DESDE GET_DATA: {signal_value_path}')
    except:
        print('First load a project')
        signal_value_path = ['None']
    finally:
        return signal_value_path


def extract_data(path):
    data = np.load(path)
    data = data.f.arr_0
    return data


def get_data(path):
    if path is not 'None':
        pool = ThreadPool(processes = 1)
        async_result = pool.apply_async(extract_data, (path,))
        data = async_result.get()
        return data


def nebula_process(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(*args, **kwargs)
        
        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func  # returning func means func can still be used normally
    
    return decorator
