import calendar
import datetime
import numpy as np

from src.controlers.channels.layout import _topo_to_sphere
from src.controlers.info import _empty_info
from src.controlers.utils import channels, _create_channels
from src.controlers.io.constants import FIFF


def b(s):
    return s.encode("latin-1")


def read_str(fid, count = 1):
    """Read string from a binary file in a python version compatible way."""
    dtype = np.dtype('>S%i' % count)
    string = fid.read(dtype.itemsize)
    data = np.frombuffer(string, dtype = dtype)[0]
    bytestr = b('').join([data[0:data.index(b('\x00')) if b('\x00') in data else count]])
    
    return str(bytestr.decode('ascii'))  # Return native str type for Py2/3


if __name__ == '__main__':
    
    strfile = r'/home/kevrodz/Documents/eeg_examples/CARLOS-N400.cnt'
    offset = 900  # Size of the 'SETUP' header.
    cnt_info = dict()
    with open(strfile, 'rb', buffering = 0) as f:
        f.seek(21) # Position to read file
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
        hand = read_str(f, 1)
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
        print(f'n_channels: {n_channels}, sfreq: {sfreq}')
        eog = 'header'
        if eog == 'header':
            f.seek(402)
            eog = [idx for idx in np.fromfile(f, dtype = 'i2', count = 2) if idx >= 0]
        print(f'eog: {eog}')
        f.seek(438)
        lowpass_toggle = np.fromfile(f, 'i1', count = 1)[0]
        highpass_toggle = np.fromfile(f, 'i1', count = 1)[0]
        print(lowpass_toggle, highpass_toggle)

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
            
        data_format = 'auto'
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
        
        print(n_samples, lowcutoff, highcutoff, event_offset, data_size, n_samples, n_bytes)
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
        print(ch_names, cals, baselines, chs, pos)

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
    print(subject_info, highpass_toggle, lowpass_toggle, n_events, event_type, event_size)
    
    if eog == 'auto':
        eog = channels(ch_names, 'EOG', eog)
    print(f'eog channels {eog}')
    ecg, emg, misc = [], [], []
    chs = _create_channels(ch_names, cals, FIFF.FIFFV_COIL_EEG, FIFF.FIFFV_EEG_CH, eog, ecg, emg, misc)
    eeg_signature = [idx for idx, ch in enumerate(chs) if ch['coil_type'] == FIFF.FIFFV_COIL_EEG]
    coords = _topo_to_sphere(pos, eeg_signature)  # Sphere coordinates
    locs = np.full((len(chs), 12), np.nan)  # Localizations array
    locs[:, :3] = coords
    for ch, loc in zip(chs, locs):  # Paired items
        ch.update(loc = loc)

    # Addd the stim channel
    chan_info = {'cal':     1.0, 'logno': len(chs) + 1, 'scanno': len(chs) + 1, 'range': 1.0, 'unit_mul': 0.,
                 'ch_name': 'STI 014', 'unit': FIFF.FIFF_UNIT_NONE, 'coord_frame': FIFF.FIFFV_COORD_UNKNOWN,
                 'loc':     np.zeros(12), 'coil_type': FIFF.FIFFV_COIL_NONE, 'kind': FIFF.FIFFV_STIM_CH}
    chs.append(chan_info)
    baselines.append(0)  # For stim channel
    cnt_info.update(baselines = np.array(baselines), n_samples = n_samples, stim_channel = stim_channel,
                    n_bytes = n_bytes)
    info.update(meas_date = meas_date, desciption = str(session_label), bads = bads, subject_info = subject_info,
                chs = chs)
    print(f'info: {info}'
          f'cnt_info: {cnt_info}')