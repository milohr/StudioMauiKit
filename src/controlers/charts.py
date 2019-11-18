# Author: Keveen Rodriguez Zapata <keveenrodriguez@gmail.com>
#
# License: GNU Lesser General Public License v3.0 (LGPLv3)
from enum import Enum, auto


class SeriesType(Enum):
    SeriesTypeLine = 0
    SeriesTypeArea = auto()
    SeriesTypeBar = auto()
    SeriesTypeStackedBar = auto()
    SeriesTypePercentBar = auto()
    SeriesTypePie = auto()
    SeriesTypeScatter = auto()
    SeriesTypeSpline = auto()
    SeriesTypeHorizontalBar = auto()
    SeriesTypeHorizontalStackedBar = auto()
    SeriesTypeHorizontalPercentBar = auto()
    SeriesTypeBoxPlot = auto()
    SeriesTypeCandlestick = auto()
