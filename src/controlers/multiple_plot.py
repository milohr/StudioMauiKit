# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)

# !/usr/bin/python
# -*- coding: utf-8 -*-


from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys

signal_name = sys.argv[1]
path = np.load(signal_name)
data2 = path.f.arr_0
nPlots, nSamples = data2.shape
print(f'Signal path to plot: {signal_name}')
print(f'Data to plot: {data2.shape}')
points2 = list()
offset = [max(data2[n, :]) + abs(min(data2[n, :])) for n in range(nPlots)]
offset[0] = 0

app = QtGui.QApplication([])

win = pg.GraphicsWindow(title="Raw EEG plot")
pg.setConfigOptions(antialias=True)

rgn = pg.LinearRegionItem([nSamples / 5., nSamples / 3.])

p2 = win.addPlot(title="All EEG points")

p2.addItem(rgn)
p2.hideAxis('left')
p2.setLabel(axis='left', text='Channels')
xax = p2.getAxis('left')

maxi = max(data2[-1, :]) * nPlots
m = maxi / nPlots
ticks = [list(zip(np.linspace(0, 0.037, nPlots), ['Ch' + str(i+1) for i in range(nPlots)]))]  # Edit the 0.037, that is incorrect
xax.setTicks(ticks)

for i in range(nPlots):
    p2.plot(data2[i, :] + offset[1] * i, pen = (i, nPlots))

win.nextColumn()

p9 = win.addPlot(title="Zoom on selected region")
p9.hideAxis('left')
for i in range(nPlots):
    p9.plot(data2[i, :] + offset[1]*i, pen = (i, nPlots))


def updatePlot():
    p9.setXRange(*rgn.getRegion(), padding=0)
    
    
def updateRegion():
    rgn.setRegion(p9.getViewBox().viewRange()[0])
    

rgn.sigRegionChanged.connect(updatePlot)
p9.sigXRangeChanged.connect(updateRegion)
updatePlot()


if __name__ == '__main__':
    
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
