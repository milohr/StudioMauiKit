# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
# Based in MNE Constants.py file (https://github.com/mne-tools/mne-python/blob/master/mne/io/constants.py)
# License: GNU Lesser General Public License v3.0 (LGPLv3)


class Bunch(dict):
    '''
    Dictionary that exposes it key as attributes
    '''
    
    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self


class BunchConst(Bunch):
    '''
    Class to prevent re-defining constats
    '''
    
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