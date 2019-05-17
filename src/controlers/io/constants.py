# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
# Based in MNE Constants.py file (https://github.com/mne-tools/mne-python/blob/master/mne/io/constants.py)
# License: GNU Lesser General Public License v3.0 (LGPLv3)


class Bunch(dict):
    """
    Dictionary that exposes it key as attributes
    """
    
    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self


class BunchConst(Bunch):
    """
    Class to prevent re-defining constats
    """
    
    def __setattr__(self, key, value):
        if key != '__dict__' and hasattr(self, key):
            raise AttributeError('Attribute "%s" already set' % key)
        super(BunchConst, self).__setattr__(key, value)


FIFF = BunchConst()

# Info on subject
FIFF.FIFFV_SUBJ_SEX_UNKNOWN = 0
FIFF.FIFFV_SUBJ_SEX_MALE = 1
FIFF.FIFFV_SUBJ_SEX_FEMALE = 2

FIFF.FIFFV_SUBJ_HAND_RIGHT = 1
FIFF.FIFFV_SUBJ_HAND_LEFT = 2

# Info on channels
FIFF.FIFF_CH_NAME_MAX_LENGTH = 15

# Coil types
FIFF.FIFFV_COIL_EEG = 1  # EEG electrode position in r0
FIFF.FIFFV_COIL_NONE = 0  # Location info contains no data

# International System of Units (SI) derived units
FIFF.FIFF_UNIT_NONE = -1
FIFF.FIFF_UNIT_HZ = 101  # Hertz
FIFF.FIFF_UNIT_V = 107  # Volt
FIFF.FIFF_UNIT_OHM = 109  # Ohm

# Channel types
FIFF.FIFFV_EEG_CH = 2
FIFF.FIFFV_STIM_CH = 3
FIFF.FIFFV_EOG_CH = 202
FIFF.FIFFV_EMG_CH = 302
FIFF.FIFFV_ECG_CH = 402
FIFF.FIFFV_MISC_CH = 502

# Coordinate frames
FIFF.FIFFV_COORD_UNKNOWN = 0
FIFF.FIFFV_COORD_HEAD = 4




