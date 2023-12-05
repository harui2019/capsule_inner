from pathlib import Path
from typing import Union, Iterable, Literal, Optional
import json

from .jsonablize import quickJSONExport, parse
from .mori.csvlist import SingleColumnCSV


def quickJSON(
    content: Iterable,
    filename: Union[str, Path],
    mode: str,
    indent: int = 2,
    encoding: str = 'utf-8',
    jsonable: bool = False,

    save_location: Union[Path, str] = Path('./'),
    mute: bool = False,
) -> None:
    """Configurable quick JSON export.

    Args:
        content (any): Content wants to be written.
        filename (str): Filename of the file.
        mode (str): Mode for :func:`open` function.
        indent (int, optional): Indent length for json. Defaults to 2.
        encoding (str, optional): Encoding method. Defaults to 'utf-8'.
        jsonablize (bool, optional): 
            Whether to transpile all object to jsonable via :func:`mori.jsonablize`. Defaults to False.
        save_location (Union[Path, str], optional): Location of files. Defaults to Path('./').
    """
    return quickJSONExport(
        content=content,
        filename=filename,
        mode=mode,
        indent=indent,
        encoding=encoding,
        jsonable=jsonable,
        save_location=save_location,
        mute=mute,
    )


def quickListCSV(
    content: Iterable,
    filename: str,
    mode: str,
    encoding: str = 'utf-8',

    secondFilenameExt: Optional[str] = None,
    jsonable: bool = False,
    save_location: Union[Path, str] = Path('./'),

    printArgs: dict = {},
) -> None:

    if not isinstance(save_location, Path):
        save_location = Path(save_location)
    if jsonable:
        content = [parse(v) for v in content]

    tmpSingleColCSV = SingleColumnCSV(content)
    openArgs = {
        'mode': mode,
        'encoding': encoding,
    }

    tmpSingleColCSV.export(
        save_location=save_location,
        name=filename,
        secondFilenameExt=secondFilenameExt,
        openArgs=openArgs,
        printArgs=printArgs,
    )


def quickRead(
    filename: Union[str, Path],
    save_location: Union[Path, str] = Path('./'),
    filetype: Literal['json', 'txt'] = 'json',

    encoding: str = 'utf-8'
) -> Union[str, dict]:
    """Quick read file.

    Args:
        filename (Union[str, Path]): Filename.
        encoding (str, optional): Encoding method. Defaults to 'utf-8'.

    Returns:
        str: Content of the file.
    """
    if not isinstance(save_location, Path):
        save_location = Path(save_location)

    if filetype == 'json':
        with open(save_location / filename, 'r', encoding=encoding) as File:
            return json.load(File)

    else:
        with open(save_location / filename, 'r', encoding=encoding) as File:
            return File.read()
