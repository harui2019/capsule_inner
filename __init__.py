from .jsonablize import Parse as jsonablize, quickJSONExport, sortHashableAhead
from .config import Configuration, defaultConfig
from .gitsync import syncControl
from .csvlist import singleColCSV

from .taglist.tagmaps import TagList, keyTupleLoads, tupleStrParse
from .taglist.quantity import quantitiesMean, tagListQuantityMean, Q

from .quick import quickJSON, quickListCSV, quickRead

__version__ = (0, 0, 5)