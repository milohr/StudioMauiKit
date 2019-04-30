import calendar
import datetime
import numpy as np


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
        f.seek(21) # Position to readd file
        patient_id = read_str(f, 20)
        patient_id = int(patient_id) if patient_id.isdigit() else 0
        print(patient_id)
        f.seek(121)
        patient_name = read_str(f, 20).split()
        last_name = patient_name[0] if len(patient_name) > 0 else ''
        first_name = patient_name[-1] if len(patient_name) > 0 else ''
        f.seek(2, 1)
        sex = read_str(f, 1)
        print(sex, patient_name,first_name, last_name)
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
        print(n_channels, sfreq)
        eog = 'header'
        if eog == 'header':
            f.seek(402)
            eog = [idx for idx in np.fromfile(f, dtype = 'i2', count = 2) if idx >= 0]
        print(eog)
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