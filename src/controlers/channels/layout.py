# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
# Based in MNE layout.py https://github.com/mne-tools/mne-python/blob/maint/0.17/mne/channels/layout.py
# License: GNU Lesser General Public License v3.0 (LGPLv3)

import numpy as np


def _topo_to_sphere(pos, eeg_signature):
    """
    Transform XY - Coordinates to sphere
    :param pos: array-like, shape (n_channels, 2)
            XY - Coordinates to transform.
    :param eeg_signature: list of int
            Indices of EEG channels that are included when calculating the sphere.
    :return: coords:  array, shape (n_channels, 3), XYZ - Coordinates
    """
    xs, ys = np.array(pos).T
    
    sqs = np.max(np.sqrt((xs[eeg_signature] ** 2) + (ys[eeg_signature] ** 2)))
    xs /= sqs  # Shape to a sphere and normalize
    ys /= sqs
    
    xs += 0.5 - np.mean(xs[eeg_signature])  # Center the points
    ys += 0.5 - np.mean(ys[eeg_signature])
    
    xs = xs * 2. - 1.  # Values ranging from -1 to 1
    ys = ys * 2. - 1.
    
    rs = np.clip(np.sqrt(xs ** 2 + ys ** 2), 0., 1.)
    alphas = np.arccos(rs)
    zs = np.sin(alphas)
    return np.column_stack([xs, ys, zs])
