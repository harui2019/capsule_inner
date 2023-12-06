import requests
import pickle
from typing import NamedTuple
from pathlib import Path


class BasicHookArguments(NamedTuple):
    url: str
    save_location: Path | str | None = None


class BasicHook(object):
    def __init__(
        self,
        url: str,
        save_location: Path | str | None = None,
    ):
        self.config = BasicHookArguments(
            url=url,
            save_location=save_location,
        )

    def save(
        self,
        save_location: Path | str = None,
    ) -> None:
        if save_location is None:
            save_location = self.config.save_location
        if save_location is None:
            raise ValueError("save_location cannot be None")

        if isinstance(save_location, str):
            save_location = Path(save_location)
        if not save_location.exists():
            raise FileNotFoundError(f"{save_location} does not exist")

        export = self.config._asdict()
        if isinstance(export["save_location"], Path):
            export["save_location"] = str(export["save_location"])

        with open(save_location, "wb") as f:
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
            print(f"Not sent with {result.status_code}, response:\n{result.json()}")

        return result

    @classmethod
    def read(
        cls,
        save_location: Path | str,
    ):
        if save_location is None:
            raise ValueError("save_location cannot be None")
        if isinstance(save_location, str):
            save_location = Path(save_location)

        if not save_location.exists():
            raise FileNotFoundError(f"{save_location} does not exist")

        export = {}
        with open(save_location, "rb") as f:
            export: dict[str, str] = pickle.load(f)

        export["save_location"] = Path(save_location)

        return cls(**export)
