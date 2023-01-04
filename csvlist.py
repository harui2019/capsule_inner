from typing import Optional, TypeVar, Union, NamedTuple
from pathlib import Path
import os
import csv
import glob

T = TypeVar('T')


class singleColCSV(list[T]):
    __version__ = (0, 3, 1)
    __name__ = 'singleCol'

    """A quick way to create .gitignore

    Args:
        list ([type]): The list of ignored items.
    """

    def __init__(
        self,
        *args,
        name: str = 'untitled',
        **kwargs,
    ) -> None:

        super().__init__(*args, **kwargs)
        self.name = name

    defaultOpenArgs = {
        'mode': 'w+',
        'encoding': 'utf-8',
    }
    defaultPrintArgs = {
    }

    class params(NamedTuple):
        openArgs: dict
        printArgs: dict
        saveLocation: Path

    @classmethod
    def paramsControl(
        cls,
        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
        saveLocation: Union[Path, str] = Path('./'),
        isReadOnly: bool = False,
    ) -> params:
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
            saveLocation (Path, optional):
                The exported location. Defaults to `Path('./')`.
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

        # saveLocation
        if isinstance(saveLocation, (Path, str)):
            saveLocation = Path(saveLocation)
        else:
            raise ValueError(
                "'saveLocation' needs to be the type of 'str' or 'Path'.")

        if not os.path.exists(saveLocation):
            raise FileNotFoundError(f"Such location not found: {saveLocation}")

        return cls.params(
            saveLocation=saveLocation,
            openArgs=openArgs,
            printArgs=printArgs
        )

    def export(
        self,
        name: Optional[str] = 'untitled',
        saveLocation: Union[Path, str] = Path('./'),
        secondFilenameExt: Optional[str] = None,

        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
    ) -> Path:
        """Export `tagMap`.

        Args:
            name (str, optional): 
                Name for this `tagMap`.
                Defaults to 'untitled'.
            saveLocation (Path): The location of file.
            additionName (Optional[str], optional): 
                Name for this `tagMap`, 
            secondFilenameExt (Optional[str], optional):
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

        Raises:
            ValueError: When filetype is not supported.

        Return:
            Path: The path of exported file.
        """

        args = self.paramsControl(
            openArgs=openArgs,
            printArgs=printArgs,
            saveLocation=saveLocation,
        )
        printArgs = args.printArgs
        openArgs = args.openArgs
        saveLocation = args.saveLocation

        if name is None:
            name = self.name

        filename = name + (
            self.__name__ if secondFilenameExt is None else f"{secondFilenameExt}"
        ) + ".csv"

        with open(saveLocation / filename, **openArgs, newline='') as ExportCsv:
            tagmapWriter = csv.writer(ExportCsv, quotechar='|')
            for v in self:
                tagmapWriter.writerow((v, ))

        return saveLocation / filename

    @classmethod
    def read(
        cls,
        name: str,
        saveLocation: Union[Path, str] = Path('./'),
        secondFilenameExt: Optional[str] = None,

        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
        whichNum: int = 0,
        notFoundRaise: bool = True,
    ):
        """Export `tagMap`.

        Args:
            name (str, optional): 
                Name for this `tagMap`.
                Defaults to 'untitled'.
            saveLocation (Path): The location of file.
            additionName (Optional[str], optional): 
                Name for this `tagMap`, 
            secondFilenameExt (Optional[str], optional):
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
            saveLocation=saveLocation,
            isReadOnly=True,
        )
        printArgs = args.printArgs
        openArgs = args.openArgs
        saveLocation = args.saveLocation

        secondFilenameExt = cls.__name__ if secondFilenameExt is None else f"{secondFilenameExt}"

        lsLoc1 = glob.glob(str(saveLocation / f"*.{secondFilenameExt}.*"))
        if len(lsLoc1) == 0:
            if notFoundRaise:
                raise FileNotFoundError(
                    f"The file '*.{secondFilenameExt}.*' not found at '{saveLocation}'.")
            else:
                return cls(name=name)

        lsLoc2 = [f for f in lsLoc1] if name is None else [
            f for f in lsLoc1 if name in f]

        if len(lsLoc2) < 1:
            if notFoundRaise:
                raise FileNotFoundError(
                    f"The file '{name}.'" + f"{secondFilenameExt}.csv"+f" not found at '{saveLocation}'.")
            else:
                return cls(name=secondFilenameExt)
        elif len(lsLoc2) > 1:
            lsLoc2 = [lsLoc2[whichNum]]
            print(
                f"The following files '{lsLoc2}' are fitting giving 'name' and 'additionName', choosing the '{lsLoc2[0]}'.")

        filename = lsLoc2[0]
        filename = Path(filename).name
        obj = None

        with open(saveLocation / filename, **openArgs, newline='') as ReadCsv:
            tagmapReaper = csv.reader(ReadCsv, quotechar='|')
            obj = cls(
                tagmapReaper,
                name=secondFilenameExt,
            )
            obj = [v[0] for v in obj]

        return obj


# class matrixCSV(list):
#     """_summary_

#     Args:
#         list (_type_): _description_
#     """
