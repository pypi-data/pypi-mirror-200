#!/usr/bin/env python
# encoding: utf-8

"""
A set of utilities to use spike Fitter

First version MAD Nov 2022
"""

"""
put some doc here
"""

from spike.plugins import Peaks
from spike.plugins import Fitter
import numpy as np
from IPython.display import display, HTML, Javascript, Markdown, Image
import ipywidgets as widgets
from ipywidgets import Layout, HBox, VBox, Label, Output, Button, Tab
import matplotlib as mpl

import spike.Interactive.INTER as I

class NMRFitter1D(I.NMRPeaker1D):
    """
    a peak-fitter for NMR experiments
    """

    def __init__(self, data, figsize=None, show=True, Debug=False):
        super().__init__(data, figsize=figsize, show=False)
        # modify tabs
        # new one
        self.bdofit = Button(description='Fit', button_style='success', layout=I.space('80px'))
        self.bdofit.on_click(self.ondofit)
        fittab = VBox([
                HBox([Label('Do fitting'), self.bdofit]),
                HBox([VBox([self.blank, self.reset, self.scale, self.done]), self.fig.canvas])
            ])
        # insert in second place
        listtabs = list(self.tabs.children)
        listtabs.insert(1,fittab)
        self.Log = widgets.Output()
        if Debug:
            listtabs.append(self.Log)
        
        # [print(t) for t in listtabs]
        self.tabs.children = listtabs
        self.tabs.set_title(0, 'Peak Picker')
        self.tabs.set_title(1, 'Peak Fitter')
        self.tabs.set_title(2, 'calibration')
        self.tabs.set_title(3, 'Peak Table')
        if Debug:
            self.tabs.set_title(4, 'Debug Log')

        if show:
            self.draw()
    
    def ondofit(self,e):
        "do the fit"
        self.ax.annotate('peaks fitted', (0.05, 0.95), xycoords='figure fraction')
        with self.Log:
            print('il faudrait faire qq chose avec',e)


