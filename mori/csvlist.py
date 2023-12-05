"""
================================================================
Single column csv file (:mod:`qurry.capsule.mori.csvlist`)
================================================================

"""
from typing import Optional, TypeVar, Union, NamedTuple
from pathlib import Path
import os
import csv
import glob

T = TypeVar('T')


class SingleColumnCSV(list[T]):
    """A single column csv file. 
    """

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

    class Params(NamedTuple):
        """Parameters for :func:`export` function.
        """
        openArgs: dict
        printArgs: dict
        save_location: Path

    @classmethod
    def params_control(
        cls,
        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
        save_location: Union[Path, str] = Path('./'),
        isReadOnly: bool = False,
    ) -> Params:
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
            save_location (Path, optional):
                The exported location. Defaults to `Path('./')`.
            isReadOnly (bool, optional):
                Is reading a file of `tagList` exportation. Defaults to False.

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

        # save_location
        if isinstance(save_location, (Path, str)):
            save_location = Path(save_location)
        else:
            raise ValueError(
                "'save_location' needs to be the type of 'str' or 'Path'.")

        if not os.path.exists(save_location):
            raise FileNotFoundError(f"Such location not found: {save_location}")

        return cls.Params(
            save_location=save_location,
            openArgs=openArgs,
            printArgs=printArgs
        )

    def export(
        self,
        name: Optional[str] = 'untitled',
        save_location: Union[Path, str] = Path('./'),
        secondFilenameExt: Optional[str] = None,

        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
    ) -> Path:
        """Export `tagList`.

        Args:
            name (str, optional): 
                Name for this `tagList`.
                Defaults to 'untitled'.
            save_location (Path): The location of file.
            additionName (Optional[str], optional): 
                Name for this `tagList`, 
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

        args = self.params_control(
            openArgs=openArgs,
            printArgs=printArgs,
            save_location=save_location,
        )
        printArgs = args.printArgs
        openArgs = args.openArgs
        save_location = args.save_location

        if name is None:
            name = self.name

        filename = name + (
            self.__name__ if secondFilenameExt is None else f"{secondFilenameExt}"
        ) + ".csv"

        with open(save_location / filename, **openArgs, newline='') as ExportCsv:
            taglistWriter = csv.writer(ExportCsv, quotechar='|')
            for v in self:
                taglistWriter.writerow((v, ))

        return save_location / filename

    @classmethod
    def read(
        cls,
        name: str,
        save_location: Union[Path, str] = Path('./'),
        secondFilenameExt: Optional[str] = None,

        openArgs: dict = defaultOpenArgs,
        printArgs: dict = defaultPrintArgs,
        whichNum: int = 0,
        notFoundRaise: bool = True,
    ):
        """Export `tagList`.

        Args:
            name (str, optional): 
                Name for this `tagList`.
                Defaults to 'untitled'.
            save_location (Path): The location of file.
            additionName (Optional[str], optional): 
                Name for this `tagList`, 
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

        args = cls.params_control(
            openArgs=openArgs,
            printArgs=printArgs,
            save_location=save_location,
            isReadOnly=True,
        )
        printArgs = args.printArgs
        openArgs = args.openArgs
        save_location = args.save_location

        secondFilenameExt = cls.__name__ if secondFilenameExt is None else f"{secondFilenameExt}"

        lsLoc1 = glob.glob(str(save_location / f"*.{secondFilenameExt}.*"))
        if len(lsLoc1) == 0:
            if notFoundRaise:
                raise FileNotFoundError(
                    f"The file '*.{secondFilenameExt}.*' not found at '{save_location}'.")
            else:
                return cls(name=name)

        lsLoc2 = [f for f in lsLoc1] if name is None else [
            f for f in lsLoc1 if name in f]

        if len(lsLoc2) < 1:
            if notFoundRaise:
                raise FileNotFoundError(
                    f"The file '{name}.'" + f"{secondFilenameExt}.csv"+f" not found at '{save_location}'.")
            else:
                return cls(name=secondFilenameExt)
        elif len(lsLoc2) > 1:
            lsLoc2 = [lsLoc2[whichNum]]
            print(
                f"The following files '{lsLoc2}' are fitting giving 'name' and 'additionName', choosing the '{lsLoc2[0]}'.")

        filename = lsLoc2[0]
        filename = Path(filename).name
        obj = None

        with open(save_location / filename, **openArgs, newline='') as ReadCsv:
            taglistReaper = csv.reader(ReadCsv, quotechar='|')
            obj = cls(
                taglistReaper,
                name=secondFilenameExt,
            )
            obj = [v[0] for v in obj]

        return obj


# class matrixCSV(list):
#     """_summary_

#     Args:
#         list (_type_): _description_
#     """
