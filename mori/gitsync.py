"""A quick way to create .gitignore
"""
import os
from pathlib import Path
from typing import Union


class GitSyncControl(list[str]):
    """A gitignore file generator."""

    __version__ = (0, 3, 2)
    """A quick way to create .gitignore

    Args:
        list ([type]): The list of ignored items.
    """

    def sync(
        self,
        filename: str,
        force: bool = False,
    ) -> bool:
        """Add file to sync.

        Args:
            filename (str): Filename.

        Returns:
            bool: The file is added to be synchronized, otherwise it's already added then return False.
        """
        line = f"!{filename}"
        if line in self:
            if force:
                self.append(line)
                return True
            return False

        self.append(line)
        return True

    def ignore(
        self,
        filename: str,
        force: bool = False,
    ) -> bool:
        """Add file to ignore from sync.

        Args:
            filename (str): Filename.

        Returns:
            bool: The file is added to be ignored, otherwise it's already added then return False.
        """
        line = f"{filename}"
        if line in self:
            if force:
                self.append(line)
                return True
            return False
        else:
            self.append(line)
            return True

    defaultOpenArgs = {
        "encoding": "utf-8",
        "mode": "w+",
    }
    defaultPrintArgs = {}

    def export(
        self,
        save_location: Union[Path, str],
        openArgs: dict = {
            "mode": "w+",
        },
        printArgs: dict = {},
    ) -> None:
        """Export .gitignore

        Args:
            save_location (Path): The location of .gitignore.
            openArgs (dict): The other arguments for :func:`open` function.
            printArgs (dict): The other arguments for :func:`print` function.

        """
        printArgs = {k: v for k, v in printArgs.items() if k != "file"}
        printArgs = {**self.defaultPrintArgs, **printArgs}
        openArgs = {k: v for k, v in openArgs.items() if k != "file"}
        openArgs = {**self.defaultOpenArgs, **openArgs}

        if isinstance(save_location, (Path)):
            ...
        elif isinstance(save_location, (str)):
            save_location = Path(save_location)
        else:
            raise TypeError("The save_location is not the type of 'str' or 'Path'.")

        if not os.path.exists(save_location):
            raise FileNotFoundError("The save_location is not found.")

        with open(save_location / f".gitignore", **openArgs) as ignoreList:
            [print(item, file=ignoreList, **printArgs) for item in self]

    def read(
        self,
        save_location: Union[Path, str],
        takeDuplicate: bool = False,
        ignoreForNotfound: bool = True,
        openArgs: dict = {},
    ) -> bool:
        """ead existed .gitignore

        Args:
            save_location (Path): The location of .gitignore.
            openArgs (dict): The other arguments for :func:`open` function.
            ignoreForNotfound (bool, optional): Mute `FileNotFoundError` when .gitignore is not found. Defaults to True.

        Raises:
            FileNotFoundError: The .gitignore is not found.

        Returns:
            bool: If the .gitignore is found.
        """
        openArgs = {k: v for k, v in openArgs.items() if k != "file"}
        openArgs = {**self.defaultOpenArgs, **openArgs}
        openArgs["mode"] = "r"

        if isinstance(save_location, (Path)):
            ...
        elif isinstance(save_location, (str)):
            save_location = Path(save_location)
        else:
            raise TypeError("The save_location is not the type of 'str' or 'Path'.")

        if os.path.exists(save_location / ".gitignore"):
            with open(save_location / f".gitignore", **openArgs) as ignoreList:
                for line in ignoreList.readlines():
                    newLine = line.strip()
                    if not newLine in self:
                        self.append(newLine)
                    elif takeDuplicate:
                        self.append(newLine)
            return True

        if not ignoreForNotfound:
            raise FileNotFoundError("The .gitignore is not found.")
        return False
