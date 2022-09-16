from pathlib import Path
from typing import Union

from .jsonablize import quickJSONExport, Parse
from .csvlist import singleColCSV

def quickJSON(
    content: any,
    filename: str,
    mode: str,
    indent: int = 2,
    encoding: str = 'utf-8',
    jsonablize: bool = False,
    
    saveLocation: Union[Path, str]= Path('./'),
) -> None:
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
    content: any,
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
        filename=filename,
        openArgs=openArgs,
        printArgs=printArgs,
    )