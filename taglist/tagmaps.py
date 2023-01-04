from typing import Optional, Iterable, Literal, Union
from pathlib import Path
from collections import defaultdict
import os
import json
import csv
import glob
import warnings

from ..jsonablize import Parse


def tupleStrParse(k: str) -> tuple:
    """Convert tuple strings to real tuple.

    Args:
        k (str): Tuplizing available string.

    Returns:
        tuple: The tuple.
    """
    if k[0] == '(' and k[-1] == ')':

        kt = [tr for tr in k[1:-1].split(", ")]
        kt2 = []
        for ktsub in kt:
            if len(ktsub) > 0:
                if ktsub[0] == '\'':
                    kt2.append(ktsub[1:-1])
                elif ktsub[0] == '\"':
                    kt2.append(ktsub[1:-1])
                elif ktsub.isdigit():
                    kt2.append(int(ktsub))
                else:
                    kt2.append(ktsub)

            else:
                ...
                
        kt2 = tuple(kt2)
        return kt2
    else:
        return k


def keyTupleLoads(o: dict) -> dict:
    """If a dictionary with string keys which read from json may originally be a python tuple, then transplies as a tuple.

    Args:
        o (dict): A dictionary with string keys which read from json.

    Returns:
        dict: Result which turns every possible string keys returning to 'tuple'.
    """

    if not isinstance(o, dict):
        return o

    ks = list(o.keys())
    for k in ks:
        if isinstance(k, str):
            kt2 = tupleStrParse(k)
            if kt2 != k:
                o[kt2] = o[k]
                del o[k]
    return o


class TagList(defaultdict):
    # TagList, checkmate - X
    """Specific data structures of :module:`qurry` like `dict[str, list[any]]`.

    >>> bla = TagList()

    >>> bla.guider('strTag1', [...])
    >>> bla.guider(('tupleTag1', ), [...])
    >>> # other adding of key and value via `.guider()`
    >>> bla
    ... {
    ...     (): [...], # something which does not specify tags.
    ...     'strTag1': [...], # something
    ...     ('tupleTag1', ): [...], 
    ...     ... # other hashable as key in python
    ... }

    """
    __version__ = (0, 3, 2)
    __name__ = 'TagList'
    protect_keys = ['_all', ()]

    def __init__(
        self,
        o: dict[str, list] = {},
        name: str = __name__,
        tupleStrTransplie: bool = True,
    ) -> None:

        if not isinstance(o, dict):
            raise ValueError(
                "Input needs to be a dict with all values are iterable.")
        super().__init__(list)
        self.__name__ = name

        o = keyTupleLoads(o) if tupleStrTransplie else o
        not_list_v = []
        for k, v in o.items():
            if isinstance(v, Iterable):
                self[k] = [vv for vv in v]
            else:
                not_list_v.append(k)
        
        if len(not_list_v) > 0:
            warnings.warn(
                f"The following keys '{not_list_v}' with the values are not list won't be added.")

    def all(self) -> list:
        d = []
        for k, v in self.items():
            if isinstance(v, list):
                d += v
        return d

    def with_all(self) -> dict[list]:
        return {
            **self,
            '_all': self.all()
        }

    def guider(
        self,
        legacyTag: Optional[any] = None,
        v: any = None,
    ) -> None:
        """

        Args:
            legacyTag (any): The tag for legacy as key.
            v (any): The value for legacy.

        Returns:
            dict: _description_
        """
        for k in self.protect_keys:
            if legacyTag == k:
                warnings.warn(f"'{k}' is a reserved key for export data.")

        if legacyTag is None:
            self[()].append(v)
        elif legacyTag in self:
            self[legacyTag].append(v)
        else:
            self[legacyTag] = [v]

    availableFileType = ['json', 'csv']
    _availableFileType = Literal['json', 'csv']
    defaultOpenArgs = {
        'mode': 'w+',
        'encoding': 'utf-8',
    }
    defaultPrintArgs = {
    }
    defaultJsonDumpArgs = {
        'indent': 2,
        'ensure_ascii': False,
    }

    @classmethod
    def paramsControl(
        cls,
        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
        jsonDumpArgs: dict = defaultJsonDumpArgs,
        saveLocation: Union[Path, str] = Path('./'),
        filetype: _availableFileType = 'json',
        isReadOnly: bool = False,
    ) -> dict[str, dict[str, str]]:
        """Handling all arguments.

        Args:
            openArgs (dict, optional): 
                The other arguments for :func:`open` function.
                Defaults to :attr:`self.defaultOpenArgs`, which is:
                >>> {
                    'mode': 'w+',
                    'encoding': 'utf-8',
                }
            printArgs (dict, optional): 
                The other arguments for :func:`print` function.
                Defaults to :attr:`self.defaultPrintArgs`, which is:
                >>> {}
            jsonDumpArgs (dict, optional): 
                The other arguments for :func:`json.dump` function.
                Defaults to :attr:`self.defaultJsonDumpArgs`, which is: 
                >>> {
                    'indent': 2,
                }
            saveLocation (Path, optional):
                The exported location. Defaults to `Path('./')`.
            filetype (Literal[&#39;json&#39;, &#39;csv&#39;], optional): 
                Export type of `tagMap`. Defaults to 'json'.
            isReadOnly (bool, optional):
                Is reading a file of `tagMap` exportation. Defaults to False.
            

        Returns:
            dict[str, dict[str, str]]: Current arguments.
        """

        # working args
        printArgs = {k: v for k, v in printArgs.items() if k != 'file'}
        printArgs = {**cls.defaultPrintArgs, **printArgs}
        openArgs = {k: v for k, v in openArgs.items() if k != 'file'}
        openArgs = {**cls.defaultOpenArgs, **openArgs}
        if isReadOnly:
            openArgs['mode'] = 'r'
        jsonDumpArgs = {k: v for k, v in jsonDumpArgs.items()
                        if k != 'obj' or k != 'fp'}
        jsonDumpArgs = {**cls.defaultJsonDumpArgs, **jsonDumpArgs}

        # saveLocation
        if isinstance(saveLocation, (Path, str)):
            saveLocation = Path(saveLocation)
        else:
            raise ValueError(
                "'saveLocation' needs to be the type of 'str' or 'Path'.")

        if not os.path.exists(saveLocation):
            raise FileNotFoundError(f"Such location not found: {saveLocation}")

        # file type check
        if not filetype in cls._availableFileType.__args__:
            raise ValueError(
                f"Instead of '{filetype}', Only {cls.availableFileType} can be exported.")

        return {
            'openArgs': openArgs,
            'printArgs': printArgs,
            'jsonDumpArgs': jsonDumpArgs,
            'saveLocation': saveLocation,
        }

    def export(
        self,
        saveLocation: Union[Path, str] = Path('./'),
        tagmapName: str = __name__,
        name: Optional[str] = None,
        filetype: _availableFileType = 'json',

        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
        jsonDumpArgs: dict = defaultJsonDumpArgs,
    ) -> Path:
        """Export `tagMap`.

        Args:
            saveLocation (Path): The location of file.
            tagmapName (str, optional): 
                Name for this `tagMap`.
                Defaults to :attr:`self.__name__`.
            additionName (Optional[str], optional): 
                Addition name for this `tagMap`, 
                when does not specify any text but `None`, then generating file name like:
                >>> f"{name}.{filetype}"
                Otherwise, :
                >>> f"{additionName}.{name}.{filetype}"
                Defaults to None.
            filetype (Literal[&#39;json&#39;, &#39;csv&#39;], optional): 
                Export type of `tagMap`. Defaults to 'json'.
            openArgs (dict, optional): 
                The other arguments for :func:`open` function.
                Defaults to :attr:`self.defaultOpenArgs`, which is:
                >>> {
                    'mode': 'w+',
                    'encoding': 'utf-8',
                }
            printArgs (dict, optional): 
                The other arguments for :func:`print` function.
                Defaults to :attr:`self.defaultPrintArgs`, which is:
                >>> {}
            jsonDumpArgs (dict, optional): 
                The other arguments for :func:`json.dump` function.
                Defaults to :attr:`self.defaultJsonDumpArgs`, which is: 
                >>> {
                    'indent': 2,
                } 

        Raises:
            ValueError: When filetype is not supported.

        Return:
            Path: The path of exported file.
        """

        args = self.paramsControl(
            openArgs=openArgs,
            printArgs=printArgs,
            jsonDumpArgs=jsonDumpArgs,
            saveLocation=saveLocation,
            filetype=filetype,
        )
        printArgs = args['printArgs']
        openArgs = args['openArgs']
        jsonDumpArgs = args['jsonDumpArgs']
        saveLocation = args['saveLocation']

        filename = (
            f"" if name is None else f"{name}.") + f"{tagmapName}.{filetype}"

        if filetype == 'json':
            with open(saveLocation / filename, **openArgs) as ExportJson:
                json.dump(Parse(self), ExportJson, **jsonDumpArgs)

        elif filetype == 'csv':
            with open(saveLocation / filename, **openArgs, newline='') as ExportCsv:
                tagmapWriter = csv.writer(ExportCsv, quotechar='|')
                for k, vs in self.items():
                    for v in vs:
                        tagmapWriter.writerow((k, v))

        else:
            warnings.warn("Exporting cancelled for no specified filetype.")

        return saveLocation / filename

    @classmethod
    def read(
        cls,
        saveLocation: Union[Path, str] = Path('./'),
        tagmapName: str = __name__,
        name: Optional[str] = None,
        filetype: _availableFileType = 'json',
        tupleStrTransplie: bool = True,

        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
        jsonDumpArgs: dict = defaultJsonDumpArgs,
        
        whichNum: int = 0,
        notFoundRaise: bool = True,
    ):
        """Export `tagMap`.

        Args:
            saveLocation (Path): The location of file.
            tagmapName (str, optional): 
                Name for this `tagMap`.
                Defaults to `tagMap`.
            additionName (Optional[str], optional): 
                Addition name for this `tagMap`, 
                when does not specify any text but `None`, then generating file name like:
                >>> f"{name}.{filetype}"
                Otherwise, :
                >>> f"{additionName}.{name}.{filetype}"
                Defaults to None.
            filetype (Literal[&#39;json&#39;, &#39;csv&#39;], optional): 
                Export type of `tagMap`. Defaults to 'json'.
            openArgs (dict, optional): 
                The other arguments for :func:`open` function.
                Defaults to :attr:`self.defaultOpenArgs`, which is:
                >>> {
                    'mode': 'w+',
                    'encoding': 'utf-8',
                }
            printArgs (dict, optional): 
                The other arguments for :func:`print` function.
                Defaults to :attr:`self.defaultPrintArgs`, which is:
                >>> {}
            jsonDumpArgs (dict, optional): 
                The other arguments for :func:`json.dump` function.
                Defaults to :attr:`self.defaultJsonDumpArgs`, which is: 
                >>> {
                    'indent': 2,
                } 

        Raises:
            ValueError: When filetype is not supported.
            FileNotFoundError: _description_
            FileNotFoundError: _description_

        Return:
            Path: The path of exported file.
        """
        args = cls.paramsControl(
            openArgs=openArgs,
            printArgs=printArgs,
            jsonDumpArgs=jsonDumpArgs,
            saveLocation=saveLocation,
            filetype=filetype,
            isReadOnly=True,
        )
        printArgs = args['printArgs']
        openArgs = args['openArgs']
        jsonDumpArgs = args['jsonDumpArgs']
        saveLocation = args['saveLocation']

        lsLoc1 = glob.glob(str(saveLocation / f"*.{tagmapName}.*"))
        if len(lsLoc1) == 0:
            if notFoundRaise:
                raise FileNotFoundError(
                    f"The file '*.{tagmapName}.*' not found at '{saveLocation}'.")
            else:
                return cls(name=tagmapName)
        lsLoc2 = [f for f in lsLoc1 if filetype in f]
        if not name is None:
            lsLoc2 = [f for f in lsLoc2 if name in f]

        if len(lsLoc2) < 1:
            if notFoundRaise:
                raise FileNotFoundError("The file "+(
                    f"" if name is None else f"{name}.") + f"{tagmapName}.{filetype}"+f" not found at '{saveLocation}'.")
            else:
                return cls(name=tagmapName)
        elif len(lsLoc2) > 1:
            lsLoc2 = [lsLoc2[whichNum]]
            print(f"The following files '{lsLoc2}' are fitting giving 'name' and 'additionName', choosing the '{lsLoc2[0]}'.")
            
        filename = lsLoc2[0]
        filename = Path(filename).name
        obj = None
            
        if filetype == 'json':
            with open(saveLocation / filename, **openArgs) as ReadJson:
                rawData = json.load(ReadJson)
                obj = cls(
                    o=rawData,
                    name=tagmapName,
                    tupleStrTransplie=tupleStrTransplie,
                )

        elif filetype == 'csv':
            with open(saveLocation / filename, **openArgs, newline='') as ReadCsv:
                tagmapReaper = csv.reader(ReadCsv, quotechar='|')
                obj = cls(
                    name=tagmapName,
                )
                for k, v in tagmapReaper:
                    kt = tupleStrParse(k) if tupleStrParse else k
                    obj[kt].append(v)

        else:
            warnings.warn("Reading cancelled for no specified filetype.")

        return obj
            
            
def TagList(*args, **kwargs):
    return TagList(*args, **kwargs)