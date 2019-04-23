''' Conversion tool from Neuroscan to .'''

# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>

from os import path
import datetime
import calendar
import numpy as np


def read_cnt(input_name: str, montage = None, eog = None, misc = None,
             ecg = None, emg = None, data_format = 'auto', date_format = None,
             preload = 'False', verbose = None):
    '''
    
    :param input_name: str
        Path to the data (raw_eeg) file.
    :param montage: str | None | Instance of montage
        Path or instance of montage containing electrode positions.
        If None, xy sensor locations are read from the header (``x_coord`` and
        ``y_coord`` in ``ELECTLOC``) and fit to a sphere. See the documentation
    :param eog: list | tuple | 'auto'
        Names of channels or list of indices that should be designated
        EOG channels. If 'header', VEOG and HEOG channels assigned in the file
        header are used. If 'auto', channel names containing 'EOG' are used.
        Defaults to empty tuple.
    :param misc: list | tuple
        Names of channels or list of indices that should be designated
        MISC channels. Defaults to empty tuple.
    :param ecg: list | tuple | 'auto'
        Names of channels or list of indices that should be designated
        ECG channels. If 'auto', the channel names containing 'ECG' are used.
        Defaults to empty tuple
    :param emg: list | tuple
        Names of channels or list of indices that should be designated
        EMG channels. If 'auto', the channel names containing 'EMG' are used.
        Defaults to empty tuple.
    :param data_format: 'auto' | 'int16' | 'int32'
        Defines the data format the data is read in. If 'auto', it is
        determined from the file header using ``numsamples`` field.
        Defaults to 'auto'.
    :param date_format: str
        Format of date in the header. Currently supports 'mm/dd/yy' (default)
        and 'dd/mm/yy'.
    :param preload: bool | str (default False)
        Preload data into memory for data manipulation and faster indexing.
        If True, the data will be preloaded into memory (fast, requires
        large amount of memory). If preload is a string, preload is the
        file name of a memory-mapped file which is used to store the data
        on the hard drive (slower, requires less memory).
    :param verbose: bool, str, int, or None
        If not None, override default verbose level
    :return: rawCNT: Instance of raw_cnt
    '''
    
    return RawCNT(input_name, montage = montage, eog = eog, misc = misc, ecg = ecg, emg = emg,
                  data_format = data_format, date_format = date_format, preload = preload, verbose = verbose)


class RawCNT(BaseRaw)