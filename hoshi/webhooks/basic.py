import requests
import pickle
from typing import NamedTuple
from pathlib import Path


class BasicHookArguments(NamedTuple):
    url: str
    saveLocation: Path | str | None = None


class BasicHook(object):
    def __init__(
        self,
        url: str,
        saveLocation: Path | str | None = None,
    ):
        self.config = BasicHookArguments(
            url=url,
            saveLocation=saveLocation,
        )

    def save(
        self,
        saveLocation: Path | str = None,
    ) -> None:

        if saveLocation is None:
            saveLocation = self.config.saveLocation
        if saveLocation is None:
            raise ValueError("saveLocation cannot be None")

        if isinstance(saveLocation, str):
            saveLocation = Path(saveLocation)
        if not saveLocation.exists():
            raise FileNotFoundError(f"{saveLocation} does not exist")

        export = self.config._asdict()
        if isinstance(export["saveLocation"], Path):
            export["saveLocation"] = str(export["saveLocation"])

        with open(saveLocation, "wb") as f:
            pickle.dump(export, f)

    def post(
        self,
        content: dict[str, str],
        header: dict[str, str],
        hide_print: bool = False,
        **kwargs,
    ) -> requests.Response:

        result = requests.post(
            self.config.url,
            json=content,
            headers=header,
            **kwargs,
        )
        if 200 <= result.status_code < 300:
            if not hide_print:
                print(f"Webhook sent {result.status_code}")
        else:
            print(
                f"Not sent with {result.status_code}, response:\n{result.json()}")

        return result

    @classmethod
    def read(
        cls,
        saveLocation: Path | str,
    ):
        if saveLocation is None:
            raise ValueError("saveLocation cannot be None")
        if isinstance(saveLocation, str):
            saveLocation = Path(saveLocation)

        if not saveLocation.exists():
            raise FileNotFoundError(f"{saveLocation} does not exist")

        export = {}
        with open(saveLocation, "rb") as f:
            export: dict[str, str] = pickle.load(f)

        export["saveLocation"] = Path(saveLocation)

        return cls(**export)
