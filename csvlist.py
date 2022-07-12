from typing import Optional, Iterable, Literal, Union
from pathlib import Path
import os
import csv
import glob
import warnings


class singleColCSV(list):
    __version__ = (0, 3, 0)
    __name__ = 'singleColCSV'
    
    """A quick way to create .gitignore

    Args:
        list ([type]): The list of ignored items.
    """

    def __init__(
        self,
        *args,
        name: str = __name__,
        **kwargs,
    ) -> None:

        super().__init__(*args, **kwargs)
        self.__name__ = name


    defaultOpenArgs = {
        'mode': 'w+',
        'encoding': 'utf-8',
    }
    defaultPrintArgs = {
    }

    @classmethod
    def paramsControl(
        cls,
        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
        saveLocation: Union[Path, str] = Path('./'),
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

        return {
            'openArgs': openArgs,
            'printArgs': printArgs,
            'saveLocation': saveLocation,
        }

    def export(
        self,
        saveLocation: Union[Path, str] = Path('./'),
        name: str = __name__,
        additionName: Optional[str] = None,

        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
    ) -> Path:
        """Export `tagMap`.

        Args:
            saveLocation (Path): The location of file.
            name (str, optional): 
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
            saveLocation=saveLocation,
        )
        printArgs = args['printArgs']
        openArgs = args['openArgs']
        saveLocation = args['saveLocation']

        filename = (
            f"" if additionName is None else f"{additionName}.") + f"{name}.csv"

        with open(saveLocation / filename, **openArgs, newline='') as ExportCsv:
            tagmapWriter = csv.writer(ExportCsv, quotechar='|')
            for v in self:
                tagmapWriter.writerow((v))

        return saveLocation / filename

    @classmethod
    def read(
        cls,
        saveLocation: Union[Path, str] = Path('./'),
        name: str = __name__,
        additionName: Optional[str] = None,
        
        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
        
        whichNum: int = 0,
        notFoundRaise: bool = True,
    ):
        """Export `tagMap`.

        Args:
            saveLocation (Path): The location of file.
            name (str, optional): 
                Name for this `singleColList`.
                Defaults to `tagMap`.
            additionName (Optional[str], optional): 
                Addition name for this `tagMap`, 
                when does not specify any text but `None`, then generating file name like:
                >>> f"{name}.{filetype}"
                Otherwise, :
                >>> f"{additionName}.{name}.{filetype}"
                Defaults to None.
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
        printArgs = args['printArgs']
        openArgs = args['openArgs']
        saveLocation = args['saveLocation']

        lsLoc1 = glob.glob(str(saveLocation / f"*.{name}.*"))
        if len(lsLoc1) == 0:
            if notFoundRaise:
                raise FileNotFoundError(
                    f"The file '*.{name}.*' not found at '{saveLocation}'.")
            else:
                return cls(name=name)
        if not additionName is None:
            lsLoc2 = [f for f in lsLoc1 if additionName in f]

        if len(lsLoc2) < 1:
            if notFoundRaise:
                raise FileNotFoundError("The file "+(
                    f"" if additionName is None else f"{additionName}.") + f"{name}.csv"+f" not found at '{saveLocation}'.")
            else:
                return cls(name=name)
        elif len(lsLoc2) > 1:
            lsLoc2 = [lsLoc2[whichNum]]
            print(f"The following files '{lsLoc2}' are fitting giving 'name' and 'additionName', choosing the '{lsLoc2[0]}'.")
            
        filename = lsLoc2[0]
        filename = Path(filename).name
        obj = None
            

        with open(saveLocation / filename, **openArgs, newline='') as ReadCsv:
            tagmapReaper = csv.reader(ReadCsv, quotechar='|')
            obj = cls(
                tagmapReaper,
                name=name,
            )

        return obj
            
            
# class CSVList(list):
#     """_summary_

#     Args:
#         list (_type_): _description_
#     """