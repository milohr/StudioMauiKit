# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)
# np.squeeze

import numpy as np
from mne.io import read_raw_cnt
from mne import events_from_annotations, Epochs, find_events

path = '/home/kevrodz/Documents/eeg_examples/CARLOS-N400-2.cnt'
raw = read_raw_cnt(path, montage = None, preload=True, stim_channel=False, verbose=None)
print(raw)
print(raw.info)
print(raw.annotations)
print(raw.info["ch_names"])
events, event_id = events_from_annotations(raw)

epochs = Epochs(raw, events, event_id=event_id)
print(epochs)
time_epochs = raw.annotations.onset
print(time_epochs)
#raw.plot()
raw2 = np.squeeze(raw.get_data())
print(raw2.shape)
print(len(epochs.events)) #Events

#events = find_events(raw, initial_event=True, consecutive=True)
#print(events)


