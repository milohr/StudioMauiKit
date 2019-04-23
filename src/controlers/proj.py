'''Projection vector'''
# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>


class ProjMixin(object):
    """Mixin class for Raw, Evoked, Epochs.
    Notes
    -----
    This mixin adds a proj attribute as a property to data containers.
    It is True if at least one proj is present and all of them are active.
    The projs might not be applied yet if data are not preloaded. In
    this case it's the _projector attribute that does the job.
    If a private _data attribute is present then the projs applied
    to it are the ones marked as active.
    A proj parameter passed in constructor of raw or epochs calls
    apply_proj and hence after the .proj attribute is True.
    As soon as you've applied the projs it will stay active in the
    remaining pipeline.
    The suggested pipeline is proj=True in epochs (it's cheaper than for raw).
    When you use delayed SSP in Epochs, projs are applied when you call
    get_data() method. They are not applied to the evoked._data unless you call
    apply_proj(). The reason is that you want to reject with projs although
    it's not stored in proj mode.
    """

    @property
    def proj(self):
        """Whether or not projections are active."""
        return (len(self.info['projs']) > 0 and
                all(p['active'] for p in self.info['projs']))

    @verbose
    def add_proj(self, projs, remove_existing=False, verbose=None):
        """Add SSP projection vectors.
        Parameters
        ----------
        projs : list
            List with projection vectors.
        remove_existing : bool
            Remove the projection vectors currently in the file.
        verbose : bool, str, int, or None
            If not None, override default verbose level (see
            :func:`mne.verbose` and :ref:`Logging documentation <tut_logging>`
            for more).
        Returns
        -------
        self : instance of Raw | Epochs | Evoked
            The data container.
        """
        if isinstance(projs, Projection):
            projs = [projs]

        if (not isinstance(projs, list) and
                not all(isinstance(p, Projection) for p in projs)):
            raise ValueError('Only projs can be added. You supplied '
                             'something else.')

        # mark proj as inactive, as they have not been applied
        projs = deactivate_proj(projs, copy=True, verbose=self.verbose)
        if remove_existing:
            # we cannot remove the proj if they are active
            if any(p['active'] for p in self.info['projs']):
                raise ValueError('Cannot remove projectors that have '
                                 'already been applied')
            self.info['projs'] = projs
        else:
            self.info['projs'].extend(projs)
        # We don't want to add projectors that are activated again.
        self.info['projs'] = _uniquify_projs(self.info['projs'],
                                             check_active=False, sort=False)
        return self

    def apply_proj(self):
        """Apply the signal space projection (SSP) operators to the data.
        Notes
        -----
        Once the projectors have been applied, they can no longer be
        removed. It is usually not recommended to apply the projectors at
        too early stages, as they are applied automatically later on
        (e.g. when computing inverse solutions).
        Hint: using the copy method individual projection vectors
        can be tested without affecting the original data.
        With evoked data, consider the following example::
            projs_a = mne.read_proj('proj_a.fif')
            projs_b = mne.read_proj('proj_b.fif')
            # add the first, copy, apply and see ...
            evoked.add_proj(a).copy().apply_proj().plot()
            # add the second, copy, apply and see ...
            evoked.add_proj(b).copy().apply_proj().plot()
            # drop the first and see again
            evoked.copy().del_proj(0).apply_proj().plot()
            evoked.apply_proj()  # finally keep both
        Returns
        -------
        self : instance of Raw | Epochs | Evoked
            The instance.
        """
        from ..epochs import BaseEpochs
        from ..evoked import Evoked
        from .base import BaseRaw
        if self.info['projs'] is None or len(self.info['projs']) == 0:
            logger.info('No projector specified for this dataset. '
                        'Please consider the method self.add_proj.')
            return self

        # Exit delayed mode if you apply proj
        if isinstance(self, BaseEpochs) and self._do_delayed_proj:
            logger.info('Leaving delayed SSP mode.')
            self._do_delayed_proj = False

        if all(p['active'] for p in self.info['projs']):
            logger.info('Projections have already been applied. '
                        'Setting proj attribute to True.')
            return self

        _projector, info = setup_proj(deepcopy(self.info), add_eeg_ref=False,
                                      activate=True, verbose=self.verbose)
        # let's not raise a RuntimeError here, otherwise interactive plotting
        if _projector is None:  # won't be fun.
            logger.info('The projections don\'t apply to these data.'
                        ' Doing nothing.')
            return self
        self._projector, self.info = _projector, info
        if isinstance(self, (BaseRaw, Evoked)):
            if self.preload:
                self._data = np.dot(self._projector, self._data)
        else:  # BaseEpochs
            if self.preload:
                for ii, e in enumerate(self._data):
                    self._data[ii] = self._project_epoch(e)
            else:
                self.load_data()  # will automatically apply
        logger.info('SSP projectors applied...')
        return self

    def del_proj(self, idx='all'):
        """Remove SSP projection vector.
        Note: The projection vector can only be removed if it is inactive
              (has not been applied to the data).
        Parameters
        ----------
        idx : int | list of int | str
            Index of the projector to remove. Can also be "all" (default)
            to remove all projectors.
        Returns
        -------
        self : instance of Raw | Epochs | Evoked
        """
        if isinstance(idx, string_types) and idx == 'all':
            idx = list(range(len(self.info['projs'])))
        idx = np.atleast_1d(np.array(idx, int)).ravel()
        if any(self.info['projs'][ii]['active'] for ii in idx):
            raise ValueError('Cannot remove projectors that have already '
                             'been applied')
        keep = np.ones(len(self.info['projs']))
        keep[idx] = False  # works with negative indexing and does checks
        self.info['projs'] = [p for p, k in zip(self.info['projs'], keep) if k]
        return self

    def plot_projs_topomap(self, ch_type=None, layout=None, axes=None):
        """Plot SSP vector.
        Parameters
        ----------
        ch_type : 'mag' | 'grad' | 'planar1' | 'planar2' | 'eeg' | None | List
            The channel type to plot. For 'grad', the gradiometers are collec-
            ted in pairs and the RMS for each pair is plotted. If None
            (default), it will return all channel types present. If a list of
            ch_types is provided, it will return multiple figures.
        layout : None | Layout | List of Layouts
            Layout instance specifying sensor positions (does not need to
            be specified for Neuromag data). If possible, the correct
            layout file is inferred from the data; if no appropriate layout
            file was found, the layout is automatically generated from the
            sensor locations. Or a list of Layout if projections
            are from different sensor types.
        axes : instance of Axes | list | None
            The axes to plot to. If list, the list must be a list of Axes of
            the same length as the number of projectors. If instance of Axes,
            there must be only one projector. Defaults to None.
        Returns
        -------
        fig : instance of matplotlib figure
            Figure distributing one image per channel across sensor topography.
        """
        if self.info['projs'] is not None or len(self.info['projs']) != 0:
            from ..viz.topomap import plot_projs_topomap
            from ..channels.layout import find_layout
            if layout is None:
                layout = []
                if ch_type is None:
                    ch_type = [ch for ch in ['meg', 'eeg'] if ch in self]
                elif isinstance(ch_type, string_types):
                    ch_type = [ch_type]
                for ch in ch_type:
                    if ch in self:
                        layout.append(find_layout(self.info, ch, exclude=[]))
                    else:
                        warn('Channel type %s is not found in info.' % ch)
            fig = plot_projs_topomap(self.info['projs'], layout, axes=axes)
        else:
            raise ValueError("Info is missing projs. Nothing to plot.")

        return fig