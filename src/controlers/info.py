# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
# Some functions was taken by MNE (https://github.com/mne-tools/mne-python/blob/master/mne)
# License: GNU Lesser General Public License v3.0 (LGPLv3)

from copy import deepcopy
import numpy as np
from src.controlers.io.constants import FIFF


class Information(dict):
    '''
    Measure information
    This works like a dictionary. It contains all metadata that is available for a recording.
    '''
    
    def copy(self):
        '''
        
        :return: Information, instance of information
                The copied information.
        '''
        return Information(deepcopy(self))
    
    def _check_ch_name_length(self):
        '''
        Checks that channels names are short
        :return: None
        '''
        bad_names = list()
        for ch in self['chs']:
            if len(ch['ch_name']) > 15:
                bad_names.append(ch['ch_name'])
                ch['ch_name'] = ch['ch_name'][:15]
        if len(bad_names) > 0:
            print('{} channel names are too long, have been truncate'
                  ' to 15 characters: {}'.format(len(bad_names), bad_names))
            self._update_redundant()
    
    def _update_redundant(self):
        '''
        Update the redundant entries
        :return: None
        '''
        self['ch_names'] = [ch['ch_name'] for ch in self['chs']]
        self['nchan'] = len(self['chs'])
    
    def _check_consistency(self):
        '''
        Consistency checks and datatype tweaks
        :return: None
        '''
        missing = [bad for bad in self['bads'] if bad not in self['ch_names']]
        if len(missing) > 0:
            raise RuntimeError('Bad channel(s) %s marked do not exist in info' % (missing,))
        meas_date = self.get('meas_date')
        if meas_date is not None and (not isinstance(self['meas_date'], tuple) or
                                      len(self['meas_date']) != 2):
            raise RuntimeError('Information["meas_date"] must be a tuple of length '
                               '2 or None, got "%r"'
                               % (repr(self['meas_date']),))
        
        chs = [ch['ch_name'] for ch in self['chs']]
        if len(self['ch_names']) != len(chs) or any(ch_1 != ch_2 for ch_1, ch_2 in zip(self['ch_names'], chs)) or \
                self['nchan'] != len(chs):
            raise RuntimeError('Information channel name inconsistency detected, '
                               'please notify it to Medula developer')
        
        for key in ('sfreq', 'highpass', 'lowpass'):  # Make sure to have the proper datatypes
            if self.get(key) is not None:
                self[key] = float(self[key])
        
        self._check_ch_name_length()  # Make sure channel names are not too long
        
        # make sure channel names are unique
        self['ch_names'] = _unique_channel_names(self['ch_names'])
        for idx, ch_name in enumerate(self['ch_names']):
            self['chs'][idx]['ch_name'] = ch_name
        
        if 'filename' in self:
            print('the "filename" key is misleading '
                  'and info should not have it')


def _unique_channel_names(ch_names):
    """Ensure unique channel names."""
    unique_ids = np.unique(ch_names, return_index = True)[1]
    if len(unique_ids) != len(ch_names):
        duplicates = set(ch_names[x]
                         for x in np.setdiff1d(range(len(ch_names)), unique_ids))
        print('Channel names are not unique, found duplicates for: {}. Applying running'
              ' numbers for duplicates.'.format(duplicates))
        for ch_stem in duplicates:
            overlaps = np.where(np.array(ch_names) == ch_stem)[0]
            # We need an extra character since we append '-'.
            # np.ceil(...) is the maximum number of appended digits.
            n_keep = (FIFF.FIFF_CH_NAME_MAX_LENGTH - 1 - int(np.ceil(np.log10(len(overlaps)))))
            n_keep = min(len(ch_stem), n_keep)
            ch_stem = ch_stem[:n_keep]
            for idx, ch_idx in enumerate(overlaps):
                ch_name = ch_stem + '-%s' % idx
                if ch_name not in ch_names:
                    ch_names[ch_idx] = ch_name
                else:
                    raise ValueError('Adding a running number for a duplicate resulted in another '
                                     'duplicate name {}'.format(ch_name))
    return ch_names


def _empty_info(sfreq):
    """Create an empty info dictionary."""
    # from ..transforms import Transform
    _none_keys = (
        'acq_pars', 'acq_stim', 'ctf_head_t', 'description',
        'dev_ctf_t', 'dig', 'experimenter',
        'file_id', 'highpass', 'hpi_subsystem', 'kit_system_id',
        'line_freq', 'lowpass', 'meas_date', 'meas_id', 'proj_id', 'proj_name',
        'subject_info', 'xplotter_layout', 'gantry_angle',
    )
    _list_keys = ('bads', 'chs', 'comps', 'events', 'hpi_meas', 'hpi_results',
                  'projs', 'proc_history')
    information = Information()
    for k in _none_keys:
        information[k] = None
    for k in _list_keys:
        information[k] = list()
    information['custom_ref_applied'] = False
    # information['dev_head_t'] = Transform('meg', 'head')
    information['highpass'] = 0.
    information['sfreq'] = float(sfreq)
    information['lowpass'] = information['sfreq'] / 2.
    information._update_redundant()
    information._check_consistency()
    return information
