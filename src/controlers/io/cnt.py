''' Read tool from Neuroscan '''

# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>

from os import path
import datetime
import calendar
import numpy as np

from src.controlers.channels.layout import _topo_to_sphere
from src.controlers.utils import read_str
from src.controlers.utils import _find_channels
from src.controlers.utils import channels
from src.controlers.utils import _create_channels
from src.controlers.io.constants import FIFF
from src.controlers.info import _empty_info


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
    :param eog: list | tuple | 'auto' | 'header'
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


def _get_cnt_info(input_name, eog, ecg, emg, misc, data_format, date_format):
    '''
    Conversion tool from Neuroscan to .
    Reading only the fields of interest. Structure of the whole header at
    http://paulbourke.net/dataformats/eeg/
    :param input_name: str
        Path to the data (raw_eeg) file.
    :param eog: list | tuple | 'auto' | 'header'
        Names of channels or list of indices that should be designated
        EOG channels. If 'header', VEOG and HEOG channels assigned in the file
        header are used. If 'auto', channel names containing 'EOG' are used.
        Defaults to empty tuple.
    :param ecg: list | tuple | 'auto'
        Names of channels or list of indices that should be designated
        ECG channels. If 'auto', the channel names containing 'ECG' are used.
        Defaults to empty tuple
    :param emg: list | tuple | 'auto'
        Names of channels or list of indices that should be designated
        EMG channels. If 'auto', the channel names containing 'EMG' are used.
        Defaults to empty tuple.
    :param misc: list | tuple
        Names of channels or list of indices that should be designated
        MISC channels. Defaults to empty tuple.
    :param data_format: 'auto' | 'int16' | 'int32'
        Defines the data format the data is read in. If 'auto', it is
        determined from the file header using ``numsamples`` field.
        Defaults to 'auto'.
    :param date_format: str
        Format of date in the header. Currently supports 'mm/dd/yy' (default)
        and 'dd/mm/yy'.
    :return: info, cnt_info
    '''
    offset = 900  # Size of the header setup
    cnt_info = dict()
    with open(input_name, 'rb', buffering = 0) as f:
        f.seek(21)  # Position to read file
        patient_id = read_str(f, 20)
        patient_id = int(patient_id) if patient_id.isdigit() else 0
        print(patient_id)
        f.seek(121)
        patient_name = read_str(f, 20).split()
        last_name = patient_name[0] if len(patient_name) > 0 else ''
        first_name = patient_name[-1] if len(patient_name) > 0 else ''
        f.seek(2, 1)
        sex = read_str(f, 1)
        print(sex, patient_name, first_name, last_name)
        if sex == 'M':
            sex = FIFF.FIFFV_SUBJ_SEX_MALE
        elif sex == 'F':
            sex = FIFF.FIFFV_SUBJ_SEX_FEMALE
        else:
            sex = FIFF.FIFFV_SUBJ_SEX_UNKNOWN
        hand = read_str(f, 1)
        if hand == 'R':
            hand = FIFF.FIFFV_SUBJ_HAND_RIGHT
        elif hand == 'L':
            hand = FIFF.FIFFV_SUBJ_HAND_LEFT
        else:  # Can be 'M' for mixed or 'U'
            hand = None
        print(hand)
        f.seek(205)
        session_label = read_str(f, 20)
        session_date = read_str(f, 10)
        time = read_str(f, 12)
        date = session_date.split('/')
        date_format = 'dd/mm/yy'
        if len(date) == 3 and len(time) == 3:
            if date[2].startswith('9'):
                date[2] = '19' + date[2]
            elif len(date[2]) == 2:
                date[2] = '20' + date[2]
            time = time.split(':')
            if date_format == 'dd/mm/yy':
                date[0], date[1] = date[1], date[0]
            elif date_format != 'mm/dd/yy':
                raise ValueError("Only date formats 'mm/dd/yy' and "
                                 "'dd/mm/yy' supported. "
                                 "Got '%s'." % date_format)
            # Assuming mm/dd/yy
            date = datetime.datetime(int(date[2]), int(date[0]),
                                     int(date[1]), int(time[0]),
                                     int(time[1]), int(time[2]))
            meas_date = (calendar.timegm(date.utctimetuple()), 0)
        else:
            print(' Could not parse meas date from the header. '
                  'Setting to None.')
            meas_date = None
        f.seek(370)
        n_channels = np.fromfile(f, dtype = '<u2', count = 1)[0]
        f.seek(376)
        sfreq = np.fromfile(f, dtype = '<u2', count = 1)[0]
        if eog == 'header':
            f.seek(402)
            eog = [idx for idx in np.fromfile(f, dtype = 'i2', count = 2) if idx >= 0]
        
        f.seek(438)
        lowpass_toggle = np.fromfile(f, 'i1', count = 1)[0]
        highpass_toggle = np.fromfile(f, 'i1', count = 1)[0]
        
        f.seek(864)
        n_samples = np.fromfile(f, dtype = '<i4', count = 1)[0]
        f.seek(869)
        lowcutoff = np.fromfile(f, dtype = 'f4', count = 1)[0]
        f.seek(2, 1)
        highcutoff = np.fromfile(f, dtype = 'f4', count = 1)[0]
        
        f.seek(886)
        event_offset = np.fromfile(f, dtype = '<i4', count = 1)[0]
        cnt_info['continuous_seconds'] = np.fromfile(f, dtype = '<f4', count = 1)[0]
        
        if event_offset < offset:  # no events
            data_size = n_samples * n_channels
        else:
            data_size = event_offset - (offset + 75 * n_channels)
        if data_format == 'auto':
            if (n_samples == 0 or
                    data_size // (n_samples * n_channels) not in [2, 4]):
                print('Could not define the number of bytes automatically. Defaulting to 2.')
                n_bytes = 2
                n_samples = data_size // (n_bytes * n_channels)
            else:
                n_bytes = data_size // (n_samples * n_channels)
        else:
            if data_format not in ['int16', 'int32']:
                raise ValueError("data_format should be 'auto', 'int16' or "
                                 "'int32'. Got %s." % data_format)
            n_bytes = 2 if data_format == 'int16' else 4
            n_samples = data_size // (n_bytes * n_channels)
        
        # Channel offset refers to the size of blocks per channel in the file.
        cnt_info['channel_offset'] = np.fromfile(f, dtype = '<i4', count = 1)[0]
        if cnt_info['channel_offset'] > 1:
            cnt_info['channel_offset'] //= n_bytes
        else:
            cnt_info['channel_offset'] = 1
        ch_names, cals, baselines, chs, pos = (list(), list(), list(), list(), list())
        bads = list()
        for ch_idx in range(n_channels):  # Electrodes fields
            f.seek(offset + 75 * ch_idx)
            ch_name = read_str(f, 10)
            ch_names.append(ch_name)
            f.seek(offset + 75 * ch_idx + 4)
            if np.fromfile(f, dtype = 'u1', count = 1)[0]:
                bads.append(ch_name)
            f.seek(offset + 75 * ch_idx + 19)
            xy = np.fromfile(f, dtype = 'f4', count = 2)
            xy[1] *= -1  # invert y-axis
            pos.append(xy)
            f.seek(offset + 75 * ch_idx + 47)
            # Baselines are subtracted before scaling the data.
            baselines.append(np.fromfile(f, dtype = 'i2', count = 1)[0])
            f.seek(offset + 75 * ch_idx + 59)
            sensitivity = np.fromfile(f, dtype = 'f4', count = 1)[0]
            f.seek(offset + 75 * ch_idx + 71)
            cal = np.fromfile(f, dtype = 'f4', count = 1)
            cals.append(cal * sensitivity * 1e-6 / 204.8)
        
        if event_offset > offset:
            f.seek(event_offset)
            event_type = np.fromfile(f, dtype = '<i1', count = 1)[0]
            event_size = np.fromfile(f, dtype = '<i4', count = 1)[0]
            if event_type == 1:
                event_bytes = 8
            elif event_type in (2, 3):
                event_bytes = 19
            else:
                raise IOError('Unexpected event size.')
            n_events = event_size // event_bytes
        else:
            n_events = 0
        
        stim_channel = np.zeros(n_samples)  # Construct stim channel
        for i in range(n_events):
            f.seek(event_offset + 9 + i * event_bytes)
            event_id = np.fromfile(f, dtype = 'u2', count = 1)[0]
            f.seek(event_offset + 9 + i * event_bytes + 4)
            offset = np.fromfile(f, dtype = '<i4', count = 1)[0]
            if event_type == 3:
                offset *= n_bytes * n_channels
            event_time = offset - 900 - 75 * n_channels
            event_time //= n_channels * n_bytes
            stim_channel[event_time - 1] = event_id
    
    info = _empty_info(sfreq)  # Create the information data
    
    if lowpass_toggle is 1:
        info['lowpass'] = highcutoff
    if highpass_toggle is 1:
        info['highpass'] = lowcutoff
    subject_info = {'id':  patient_id, 'first_name': first_name, 'last_name': last_name,
                    'sex': sex, 'hand': hand}
    
    # Channels treatment
    if eog == 'auto':
        eog = _find_channels(ch_names, 'EOG')
        #eog = channels(ch_names, 'EOG', eog)
    if ecg == 'auto':
        ecg = _find_channels(ch_names, 'ECG')
        #ecg = channels(ch_names, 'ECG', ecg)
    if emg == 'auto':
        emg = _find_channels(ch_names, 'EMG')
        #emg = channels(ch_names, 'EMG', emg)

    chs = _create_channels(ch_names, cals, FIFF.FIFFV_COIL_EEG, FIFF.FIFFV_EEG_CH, eog, ecg, emg, misc)
    eeg_signature = [idx for idx, ch in enumerate(chs) if ch['coil_type'] == FIFF.FIFFV_COIL_EEG]
    coords = _topo_to_sphere(pos, eeg_signature)  # Sphere coordinates
    locs = np.full((len(chs), 12), np.nan)  # Localizations array
    locs[:, :3] = coords
    for ch, loc in zip(chs, locs):  # Paired items
        ch.update(loc=loc)
    
    # Addd the stim channel
    chan_info = {'cal': 1.0, 'logno': len(chs) + 1, 'scanno': len(chs) + 1, 'range': 1.0, 'unit_mul': 0.,
                 'ch_name': 'STI 014', 'unit': FIFF.FIFF_UNIT_NONE, 'coord_frame': FIFF.FIFFV_COORD_UNKNOWN,
                 'loc': np.zeros(12), 'coil_type': FIFF.FIFFV_COIL_NONE, 'kind': FIFF.FIFFV_STIM_CH}
    chs.append(chan_info)
    baselines.append(0)  # For stim channel
    cnt_info.update(baselines=np.array(baselines), n_samples=n_samples, stim_channel=stim_channel, n_bytes=n_bytes)
    info.update(meas_date=meas_date, desciption=str(session_label), bads=bads, subject_info=subject_info, chs=chs)
    return info, cnt_info


class RawCNT:
    
    def __init__(self, input_name, montage, eog = 'auto', misc = None, ecg = 'auto', emg = 'auto',
                 data_format = 'auto', date_format = None, preload = False, verbose = None):
        input_name = path.abspath(input_name)
        info, cnt_info = _get_cnt_info(input_name, eog, ecg, emg, misc,
                                       data_format = 'auto', date_format = 'dd/mm/yy')
        last_samples = [cnt_info['n_samples'] - 1]
        # super(RawCNT, self).__init__(info, preload, filenames=[input_name], raw_extras=[cnt_info],
        #                              last_samples=last_samples, orig_format='int', verbose=verbose)


