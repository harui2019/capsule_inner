from typing import NamedTuple, Optional, Callable, Iterable, Any
from collections import namedtuple
from ..jsonablize import Parse as jsonablize


class DefaultConfig():
    __version__ = (0, 2, 0)

    def __init__(
        self,
        default: dict[str, Any] = {},
        name: str = "defaultConfig",
        default_names: Iterable[str] = [],
    ) -> None:
        """Set the default parameters dictionary for multiple experiment.

        A replacement of :cls:`Configuration`.

        Args:
            default (Optional[dict[Any]], optional): [description]. Defaults to None.
            name (str, optional): [description]. Defaults to 'configuration'.
        """

        self.__name__ = name
        self.default = {}

        for k in default_names:
            self.default[k] = None
        for k in default:
            self.default[k] = default[k]

        self.namedtupleType = namedtuple(
            field_names=self.default.keys(),
            typename=self.__name__,
            defaults=self.default.values(),
        )
        self.default_names = self.namedtupleType._fields

    def __call__(
        self,
        *args,
        **kwargs
    ) -> Callable:

        return self.make(*args, **kwargs)

    def __getitem__(self, key) -> Any:
        return self.default[key]

    def __iter__(self):
        for k, v in self.default.items():
            yield k, v

    def _handle_input(
        self,
        inputObject: Optional[dict[Any]] = None
    ) -> None:
        """Check the input for :meth:`.check` and :meth:`.ready`.

        Args:
            inputObject (Optional[dict[Any]], optional): 
                Input. Defaults to None.

        Raises:
            ValueError: When Input is None.
            TypeError: When Input is not a dict.
        """

        if inputObject == None:
            raise ValueError("Input can not be null.")
        elif isinstance(inputObject, dict):
            ...
        else:
            raise TypeError("Input must be a dict.")

    def make(
        self,
        __values: dict[str, Any] = {},
        *args: list[str],
        partial: list[str] = [],
        jsonable: bool = False,
    ) -> dict[str, Any]:
        """Export a dictionary of configuration.

        Args:
            __values (dict[str, Any], optional): Additonal object. Defaults to `{}`.
            args (list[str], optional): Positional arguments handler.
            partial (list[str], optional): Export parts of configuration. Defaults to `[]` as exporting all.
            jsonable (bool, optional): Whether to make the configuration jsonable. Defaults to `False`.

        Returns:
            dict[str, Any]: A dictionary of configuration.
        """
        if len(args) > 0:
            raise ValueError(
                "Only allow one positional argument to be passed, which is dictionary for configuration.")

        config = {
            **self.default,
            **__values,
        }

        if jsonable:
            config = jsonablize(config)

        if len(partial) == 0:
            return config
        else:
            return {
                k: v for k, v in config.items()
                if k in partial
            }

    def as_dict(self, *args, **kwargs) -> dict[str, Any]:
        """Export configuration as a dictionary, the alternative name of :method:`make`.

        Args:
            __values (dict[str, Any], optional): Additonal object. Defaults to `{}`.
            args (list[str], optional): Positional arguments handler.
            partial (list[str], optional): Export parts of configuration. Defaults to `[]` as exporting all.
            jsonable (bool, optional): Whether to make the configuration jsonable. Defaults to `False`.

        Returns:
            dict[str, Any]: A dictionary of configuration.
        """
        return self.make(*args, **kwargs)

    def as_namedtuple(
        self,
        __values: dict[str, Any] = {},
    ) -> NamedTuple:
        """Export configuration as a namedtuple.

        Args:
            __values (dict[str, Any], optional): _description_. Defaults to {}.

        Returns:
            _type_: _description_
        """

        return self.namedtupleType(**__values)

    def is_ready(
        self,
        target: dict[str, Any] = {},
        ignores: list[str] = [],
    ) -> bool:
        """Check whether the configuration is completed.

        Args:
            target (dict): The configuration want to check. Defaults to {}.
            ignores (list[str], optional): The keys to be ignored. Defaults to [].

        Returns:
            bool: Whether the configuration is completed
        """
        self._handle_input(target)
        return all(k in target or k in ignores for k in self.namedtupleType._fields)

    def conclude_keys(
        self,
        target: dict[str, Any] = {},
        excepts: list[str] = [],
    ) -> dict[str, list[str]]:
        """Giving the list of keys include and exclude in the configuration from the given dictionary.

        Args:
            target (dict): The configuration want to check. Defaults to {}.
            excepts (list[str], optional): The exceptions. Defaults to [].

        Returns:
            dict[str, list[str]]: The contained and uncontained keys of the configuration.
        """
        self._handle_input(target)
        includes = []
        excludes = []
        for k in self.namedtupleType._fields:
            if (k in target or k in excepts):
                includes.append(k)
            else:
                excludes.append(k)

        return {'include': includes, 'exclude': excludes}

    def exclude_keys(
        self,
        target: dict[str, Any] = {},
        excepts: list[str] = [],
    ) -> list[str]:
        """Giving the list of keys include in the configuration from the given dictionary.

        Args:
            target (dict): The configuration want to check. Defaults to {}.
            excepts (list[str], optional): The exceptions. Defaults to [].

        Returns:
            list: The uncontained keys of the configuration.
        """
        return self.conclude_keys(target, excepts)['exclude']

    def include_keys(
        self,
        target: dict[str, Any] = {},
        excepts: list[str] = [],
    ) -> list[str]:
        """Giving the list of keys include in the configuration from the given dictionary.

        Args:
            target (dict): The configuration want to check. Defaults to {}.
            excepts (list[str], optional): The exceptions. Defaults to [].

        Returns:
            list: The contained keys of the configuration.
        """
        return self.conclude_keys(target, excepts)['include']

    def useless_keys(
        self,
        target: dict[str, Any] = {},
        ignores: list[str] = [],
    ) -> list[str]:
        """Giving the list of keys which is useless from the given dictionary.

        Args:
            target (dict): The configuration want to check. Defaults to {}.
            ignores (list[str], optional): The fields to be ignored. Defaults to [].

        Returns:
            list: The contained keys of the configuration.
        """
        self._handle_input(target)
        uselesskeylist = []
        for k in target:
            if not (k in self.namedtupleType._fields or k in ignores):
                uselesskeylist.append(k)

        return uselesskeylist

    def __repr__(self):
        return f"{self.namedtupleType()}"
