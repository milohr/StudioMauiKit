import numpy as np
from src.controlers.io.constants import FIFF


def b(s):
    return s.encode("latin-1")


def read_str(fid, count = 1):
    """
    Read string from a different ascii/binary format file in a python version compatible way.
    :param fid: File path
    :param count: number of line to start
    :return: string of info
    """
    dtype = np.dtype('>S%i' % count)  # Zero-terminate bytes and number (count)integer
    string = fid.read(dtype.itemsize)
    data = np.frombuffer(string, dtype = dtype)[0]  # Make data readeable
    bytestr = b('').join([data[0:data.index(b('\x00')) if b('\x00') in data else count]])  # Join all the data until the end
    
    return str(bytestr.decode('ascii'))

def _find_channels(ch_names, ch_type):
    """
    Find a specific channel
    :param ch_names: Array-list of channels names
    :param ch_type: Channel name, or channel type
    :return: Channel
    """
    subtuple = (ch_names,)
    subtuple = [i.upper() for i in subtuple]
    if ch_type == 'EOG':
        subtuple = ('EOG', 'EYE')
    ch_idx = [idx for idx, ch in enumerate(ch_names) if any(st in ch.upper() for st in subtuple)]
    return ch_idx


def channels(ch_names, ch_type, ch_value):
    """
    FInf type specific channels
    :param ch_names: Array-list of channels names
    :param ch_type: EOG | ECG | EMG, Channel name, or channel type
    :param ch_value: Channel value
    :return: Channel
    """
    if ch_type == 'EOG' and ch_value == 'auto':
        eog = _find_channels(ch_names, 'EOG')
        return eog
    if ch_type == 'ECG' and ch_value == 'auto':
        ecg = _find_channels(ch_names, 'ECG')
        return ecg
    if ch_type == 'EMG' and ch_value == 'auto':
        emg = _find_channels(ch_names, 'EMG')
        return emg


def _create_channels(ch_names, cals, ch_coil, ch_kind, eog, ecg, emg, misc):
    """
    Initialize info['chs'] for eeg channels
    :return: channels
    """
    channels = list()
    print(ch_names)
    for idx, ch_name in enumerate(ch_names):
        if ch_name in eog or idx in eog:
            coil_type = FIFF.FIFFV_COIL_NONE
            kind = FIFF.FIFFV_EOG_CH
        elif ch_name in ecg or idx in ecg:
            coil_type = FIFF.FIFFV_COIL_NONE
            kind = FIFF.FIFFV_ECG_CH
        elif ch_name in emg or idx in emg:
            coil_type = FIFF.FIFFV_COIL_NONE
            kind = FIFF.FIFFV_EMG_CH
        elif ch_name in misc or idx in misc:
            coil_type = FIFF.FIFFV_COIL_NONE
            kind = FIFF.FIFFV_MISC_CH
        else:
            coil_type = ch_coil
            kind = ch_kind
        
        channel_info = {'cal': cals[idx], 'logno': idx + 1, 'scanno': idx + 1, 'range': 1.0,
                        'unit_mul': 0, 'ch_name': ch_name, 'unit': FIFF.FIFF_UNIT_V,
                        'coord_frame': FIFF.FIFFV_COORD_HEAD, 'coil_type': coil_type, 'kind': kind,
                        'loc': np.zeros(12)}
        channels.append(channel_info)
    return channels
