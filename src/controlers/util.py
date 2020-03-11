# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)
from PySide2.QtCore import QSettings
from functools import wraps
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

    list_path = [QUrl(i).toLocalFile() for i in path]


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
