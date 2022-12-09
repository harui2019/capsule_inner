from .argrecord import argdict, attributedDict
from .jsonablize import Parse as jsonablize, quickJSONExport, sortHashableAhead
from .config import Configuration, defaultConfig
from .gitsync import syncControl
from .csvlist import singleColCSV

from .tagmaps.tagmaps import TagMap, keyTupleLoads, tupleStrParse
from .tagmaps.quantity import quantitiesMean, tagMapQuantityMean, Q

from .quick import quickJSON, quickListCSV, quickRead

__version__ = (0, 0, 4)