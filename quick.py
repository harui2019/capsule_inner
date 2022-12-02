from pathlib import Path
from typing import Union, Iterable

from .jsonablize import quickJSONExport, Parse
from .csvlist import singleColCSV

def quickJSON(
    content: Iterable,
    filename: Union[str, Path],
    mode: str,
    indent: int = 2,
    encoding: str = 'utf-8',
    jsonablize: bool = False,
    
    saveLocation: Union[Path, str]= Path('./'),
) -> None:
    """Configurable quick JSON export.

    Args:
        content (any): Content wants to be written.
        filename (str): Filename of the file.
        mode (str): Mode for :func:`open` function.
        indent (int, optional): Indent length for json. Defaults to 2.
        encoding (str, optional): Encoding method. Defaults to 'utf-8'.
        jsonablize (bool, optional): Whether to transpile all object to jsonable via :func:`mori.jsonablize`. Defaults to False.
        saveLocation (Union[Path, str], optional): Location of files. Defaults to Path('./').
    """    
    return quickJSONExport(
        content=content,
        filename=filename,
        mode=mode,
        indent=indent,
        encoding=encoding,
        jsonablize=jsonablize,
        saveLocation=saveLocation
    )

def quickListCSV(
    content: Iterable,
    filename: str,
    mode: str,
    encoding: str = 'utf-8',
    jsonablize: bool = False,
    saveLocation: Union[Path, str]= Path('./'),
    
    printArgs: dict = {},
) -> None:
    
    if not isinstance(saveLocation, Path):
        saveLocation = Path(saveLocation)
    if jsonablize:
        content = [Parse(v) for v in content]
        
    tmpSingleColCSV = singleColCSV(content)
    openArgs= {
        'mode': mode,
        'encoding': encoding,
    }
    
    tmpSingleColCSV.export(
        saveLocation=saveLocation,
        name=filename,
        openArgs=openArgs,
        printArgs=printArgs,
    )