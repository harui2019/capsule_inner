"""

================================================================
JSONablize (:mod:`qurry.qurry.capsule.jsonablize`)
================================================================

"""

import os
from typing import Hashable, Union, Iterable, Any
import json
from collections import OrderedDict
from pathlib import Path


def value_parse(v: Any) -> Union[Iterable, str, int, float, bool, None]:
    """Make value json-allowable. If a value is not allowed by json, them return its '__str__'.

    Args:
        v (any): Value.

    Returns:
        any: Json-allowable value.
    """

    try:
        json.dumps(v)
        return v
    except TypeError:
        return str(v)


def key_parse(k: Any) -> Union[str, int, float, bool, None]:
    """Make key json-allowable. If a value is not allowed by json, them return its '__str__'.

    str, int, float, bool or None

    Args:
        o (any): Key.

    Returns:
        any: Json-allowable key.
    """

    if isinstance(k, (str, int, float, bool)):
        parsed = k
    elif k is None:
        parsed = k
    else:
        parsed = str(k)

    return parsed


def parse(o: Any) -> Any:
    """Make a python object json-allowable.

    Args:
        o (any): Python object.

    Returns:
        any: Json-allowable python object.
    """

    if isinstance(o, list):
        parsed = [parse(v) for v in o]
    elif isinstance(o, tuple):
        parsed = [parse(v) for v in o]
    elif isinstance(o, dict):
        parsed = {key_parse(k): parse(v) for k, v in o.items()}
    else:
        parsed = value_parse(o)

    return parsed


def sort_hashable_ahead(o: dict) -> dict:
    """Make hashable values be the ahead in dictionary."

    Args:
        o (dict): Unsorted dictionary.

    Returns:
        dict: Sorted dictionary.
    """
    sort_o = OrderedDict()
    for k, v in o.items():
        if isinstance(v, Hashable):
            sort_o[k] = v

    for k, v in o.items():
        if not k in sort_o:
            sort_o[k] = v

    return sort_o


# pylint: disable=invalid-name
def quickJSONExport(
    content: Iterable,
    filename: Union[str, Path],
    mode: str,
    indent: int = 2,
    encoding: str = "utf-8",
    jsonable: bool = False,
    save_location: Union[Path, str] = Path("./"),
    mute: bool = False,
) -> None:
    """Quickly export a json file.

    Args:
        content (Iterable):
            The content of json file.
        filename (Union[str, Path]):
            The filename of json file.
        mode (str):
            The mode of open.
        indent (int, optional):
            The indent of json file. Defaults to 2.
        encoding (str, optional):
            The encoding of json file. Defaults to "utf-8".
        jsonable (bool, optional):
            Is the content jsonable. Defaults to False.
        save_location (Union[Path, str], optional):
            The location of json file. Defaults to Path("./").
        mute (bool, optional):
            Is mute the exportation. Defaults to False.
    """

    if not isinstance(save_location, Path):
        save_location = Path(save_location)
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    save_loc_w_name = save_location / filename

    with open(save_loc_w_name, mode, encoding=encoding) as file:
        if jsonable:
            json.dump(parse(content), file, indent=indent, ensure_ascii=False)
        else:
            json.dump(content, file, indent=indent, ensure_ascii=False)
        if not mute:
            print(f"'{save_loc_w_name}' exported successfully.")


# pylint: enable=invalid-name
