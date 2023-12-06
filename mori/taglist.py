from typing import Optional, Iterable, Literal, Union, TypeVar, Hashable
from pathlib import Path
from collections import defaultdict
import os
import json
import csv
import glob
import warnings

from ..jsonablize import parse

K = TypeVar("K")
T = TypeVar("T")


def tupleStrParse(k: str) -> tuple:
    """Convert tuple strings to real tuple.

    Args:
        k (str): Tuplizing available string.

    Returns:
        tuple: The tuple.
    """
    if k[0] == "(" and k[-1] == ")":
        kt = [tr for tr in k[1:-1].split(", ")]
        kt2 = []
        for ktsub in kt:
            if len(ktsub) > 0:
                if ktsub[0] == "'":
                    kt2.append(ktsub[1:-1])
                elif ktsub[0] == '"':
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


class TagList(defaultdict[Hashable, list[T]]):
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
    __name__ = "TagList"
    protect_keys = ["_all", ()]

    def __init__(
        self,
        o: dict[str, list] = {},
        name: str = __name__,
        tupleStrTransplie: bool = True,
    ) -> None:
        if not isinstance(o, dict):
            raise ValueError("Input needs to be a dict with all values are iterable.")
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
                f"The following keys '{not_list_v}' with the values are not list won't be added."
            )

    def all(self) -> list:
        d = []
        for k, v in self.items():
            if isinstance(v, list):
                d += v
        return d

    def with_all(self) -> dict[list]:
        return {**self, "_all": self.all()}

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

    availableFileType = ["json", "csv"]
    _availableFileType = Literal["json", "csv"]
    defaultOpenArgs = {
        "mode": "w+",
        "encoding": "utf-8",
    }
    defaultPrintArgs = {}
    defaultJsonDumpArgs = {
        "indent": 2,
        "ensure_ascii": False,
    }

    @classmethod
    def paramsControl(
        cls,
        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
        jsonDumpArgs: dict = defaultJsonDumpArgs,
        save_location: Union[Path, str] = Path("./"),
        filetype: _availableFileType = "json",
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
            save_location (Path, optional):
                The exported location. Defaults to `Path('./')`.
            filetype (Literal[&#39;json&#39;, &#39;csv&#39;], optional):
                Export type of `tagList`. Defaults to 'json'.
            isReadOnly (bool, optional):
                Is reading a file of `tagList` exportation. Defaults to False.


        Returns:
            dict[str, dict[str, str]]: Current arguments.
        """

        # working args
        printArgs = {k: v for k, v in printArgs.items() if k != "file"}
        printArgs = {**cls.defaultPrintArgs, **printArgs}
        openArgs = {k: v for k, v in openArgs.items() if k != "file"}
        openArgs = {**cls.defaultOpenArgs, **openArgs}
        if isReadOnly:
            openArgs["mode"] = "r"
        jsonDumpArgs = {
            k: v for k, v in jsonDumpArgs.items() if k != "obj" or k != "fp"
        }
        jsonDumpArgs = {**cls.defaultJsonDumpArgs, **jsonDumpArgs}

        # save_location
        if isinstance(save_location, (Path, str)):
            save_location = Path(save_location)
        else:
            raise ValueError("'save_location' needs to be the type of 'str' or 'Path'.")

        if not os.path.exists(save_location):
            raise FileNotFoundError(f"Such location not found: {save_location}")

        # file type check
        if not filetype in cls._availableFileType.__args__:
            raise ValueError(
                f"Instead of '{filetype}', Only {cls.availableFileType} can be exported."
            )

        return {
            "openArgs": openArgs,
            "printArgs": printArgs,
            "jsonDumpArgs": jsonDumpArgs,
            "save_location": save_location,
        }

    def export(
        self,
        save_location: Union[Path, str] = Path("./"),
        tagListName: str = __name__,
        name: Optional[str] = None,
        filetype: _availableFileType = "json",
        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
        jsonDumpArgs: dict = defaultJsonDumpArgs,
    ) -> Path:
        """Export `tagList`.

        Args:
            save_location (Path): The location of file.
            tagListName (str, optional):
                Name for this `tagList`.
                Defaults to :attr:`self.__name__`.
            additionName (Optional[str], optional):
                Addition name for this `tagList`,
                when does not specify any text but `None`, then generating file name like:
                >>> f"{name}.{filetype}"
                Otherwise, :
                >>> f"{additionName}.{name}.{filetype}"
                Defaults to None.
            filetype (Literal[&#39;json&#39;, &#39;csv&#39;], optional):
                Export type of `tagList`. Defaults to 'json'.
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
            save_location=save_location,
            filetype=filetype,
        )
        printArgs = args["printArgs"]
        openArgs = args["openArgs"]
        jsonDumpArgs = args["jsonDumpArgs"]
        save_location = args["save_location"]

        filename = (f"" if name is None else f"{name}.") + f"{tagListName}.{filetype}"

        if filetype == "json":
            with open(save_location / filename, **openArgs) as ExportJson:
                json.dump(parse(self), ExportJson, **jsonDumpArgs)

        elif filetype == "csv":
            with open(save_location / filename, **openArgs, newline="") as ExportCsv:
                tagListWriter = csv.writer(ExportCsv, quotechar="|")
                for k, vs in self.items():
                    for v in vs:
                        tagListWriter.writerow((k, v))

        else:
            warnings.warn("Exporting cancelled for no specified filetype.")

        return save_location / filename

    @classmethod
    def read(
        cls,
        save_location: Union[Path, str] = Path("./"),
        tagListName: str = __name__,
        name: Optional[str] = None,
        filetype: _availableFileType = "json",
        tupleStrTransplie: bool = True,
        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
        jsonDumpArgs: dict = defaultJsonDumpArgs,
        whichNum: int = 0,
        notFoundRaise: bool = True,
    ):
        """Export `tagList`.

        Args:
            save_location (Path): The location of file.
            tagListName (str, optional):
                Name for this `tagList`.
                Defaults to `tagList`.
            additionName (Optional[str], optional):
                Addition name for this `tagList`,
                when does not specify any text but `None`, then generating file name like:
                >>> f"{name}.{filetype}"
                Otherwise, :
                >>> f"{additionName}.{name}.{filetype}"
                Defaults to None.
            filetype (Literal[&#39;json&#39;, &#39;csv&#39;], optional):
                Export type of `tagList`. Defaults to 'json'.
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
            save_location=save_location,
            filetype=filetype,
            isReadOnly=True,
        )
        printArgs = args["printArgs"]
        openArgs = args["openArgs"]
        jsonDumpArgs = args["jsonDumpArgs"]
        save_location = args["save_location"]

        lsLoc11 = glob.glob(str(save_location / f"{tagListName}.*"))
        lsLoc12 = glob.glob(str(save_location / f"*.{tagListName}.*"))
        if len(lsLoc11) == 0 and len(lsLoc12) == 0:
            lsLoc1 = []
        elif len(lsLoc11) == 0:
            lsLoc1 = lsLoc12
        elif len(lsLoc12) == 0:
            lsLoc1 = lsLoc11
        else:
            lsLoc1 = lsLoc11 + lsLoc12

        if len(lsLoc1) == 0:
            if notFoundRaise:
                raise FileNotFoundError(
                    f"The file '*.{tagListName}.*' not found at '{save_location}'."
                )
            else:
                return cls(name=tagListName)
        lsLoc2 = [f for f in lsLoc1 if filetype in f]
        if not name is None:
            lsLoc2 = [f for f in lsLoc2 if name in f]

        if len(lsLoc2) < 1:
            if notFoundRaise:
                raise FileNotFoundError(
                    "The file "
                    + (f"" if name is None else f"{name}.")
                    + f"{tagListName}.{filetype}"
                    + f" not found at '{save_location}'."
                )
            else:
                return cls(name=tagListName)
        elif len(lsLoc2) > 1:
            lsLoc2 = [lsLoc2[whichNum]]
            print(
                f"The following files '{lsLoc2}' are fitting giving 'name' and 'additionName', choosing the '{lsLoc2[0]}'."
            )

        filename = lsLoc2[0]
        filename = Path(filename).name
        obj = None

        if filetype == "json":
            with open(save_location / filename, **openArgs) as ReadJson:
                rawData = json.load(ReadJson)
                obj = cls(
                    o=rawData,
                    name=tagListName,
                    tupleStrTransplie=tupleStrTransplie,
                )

        elif filetype == "csv":
            with open(save_location / filename, **openArgs, newline="") as ReadCsv:
                tagListReaper = csv.reader(ReadCsv, quotechar="|")
                obj = cls(
                    name=tagListName,
                )
                for k, v in tagListReaper:
                    kt = tupleStrParse(k) if tupleStrParse else k
                    obj[kt].append(v)

        else:
            warnings.warn("Reading cancelled for no specified filetype.")

        return obj
