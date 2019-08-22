# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)


def extract_name(path):
    """
    Extract the name from a path
    :param str: Path, having in the end of the line the name to extract with the .conf format
    :return: name
    """
    import os
    head_tail = os.path.split(path)
    name = head_tail[1].replace(".conf", "")
    del head_tail
    return name


def read_raw(path):
    """

    :rtype: object
    :param path: Path of the files that contain the signal
    :return:
    """
    from PySide2.QtCore import QUrl
    from mne.io import read_raw_cnt
    import numpy as np
    import os
    #list_path = path.split(',')
    list_path = [QUrl(i).toLocalFile() for i in path]
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
        value_path = []
        # Values in a numpy array in a dict way
        raw2np = {i: np.squeeze(raw[i].get_data()) for i in raw}
        for keys in raw2np.keys():
            print(f'\033[1;32;40m Key: {keys} \033[0m \n ')
            print(f'\033[1;35;40m Values: {raw2np[keys]} \033[0m \n')
            np_path = str(keys).replace('.cnt', '.npz')
            print('Path keys ', np_path)
            np.savez_compressed(np_path, raw2np[keys])
            print(np.load(np_path)) # Organizar esto en otro hilo pero bien organizado para cargarlo despues
            value_path.append(os.path.join(os.getcwd(), str(keys) + '.npz'))
            b.append(np.load(np_path))  # List with the values, each position is a different file
        
        print(value_path)
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

