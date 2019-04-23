''' Conversion tool from Neuroscan to .'''

# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>

from os import path
import datetime
import calendar
import numpy as np

def read_cnt(input_name: str, montage=None, eog=None, misc=None, ecg=None, emg=None, data_format=None, date_format: str, preload: bool, verbose=None):
    '''
    
    :param input_name: 
    :param montage:
    :param eog:
    :param misc:
    :param ecg:
    :param emg:
    :param data_format:
    :param date_format:
    :param preload:
    :param verbose:
    :return:
    '''
    
    return RawCNT(input_name, montage=montage, eog=eog, misc=misc, ecg=ecg, emg=emg, data_format=data_format, date_format=date_format, preload=preload, verbose=verbose)