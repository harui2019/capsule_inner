from typing import NamedTuple, Union, Optional, Callable, Iterable
from collections import namedtuple
from .jsonablize import Parse as jsonablize

class Configuration(dict):
    __version__ = (0, 1, 0)
    def __init__(
        self,
        default: dict = {},
        name: str = 'configuration'
    ) -> None:
        """Set the default parameters dictionary for multiple experiment.

        In future, with the rebuilding of :meth:`multiOuput`, :meth:`powerOutput`
        :cls:`Configuration` will replace by :cls:`attributedDict`, a better data structure made by :cls:`namedtuple`.

        Args:
            default (Optional[dict[any]], optional): [description]. Defaults to None.
            name (str, optional): [description]. Defaults to 'configuration'.
        """

        self.__name__ = name
        self.default = default
        super().__init__(self.default)

    @staticmethod
    def paramsCollectList(
        collect: list[Union[int, list[int], dict[str, int]]]
    ) -> list[list[int]]:
        collectA = []
        for aItem in collect:
            if type(aItem) == list:
                collectA.append(aItem)
            elif type(aItem) == dict:
                collectA.append(aItem)
            elif type(aItem) == int:
                collectA.append([aItem])
            else:
                print(
                    f"Unrecognized type of input '{type(aItem)}'" +
                    " of '{aItem}' has been dropped.'")
        return collectA

    @staticmethod
    def typeCheck(
        target: any,
        typeWantAndHandle: list[tuple[type, Union[type, Callable]]]
    ) -> Union[Exception, any]:
        """Check whether the parameter is the type which required, then  
        transform into another type or handle it with specific function.

        Args:
            target (any): The parameter
            typeWantAndHandle (list[tuple[type, Union[type, Callable]]]): 
                The required type and the 

        Raises:
            TypeError: When there is no type which meet the requirement.

        Returns:
            Union[Exception, any]: The result of handle the parameter or 
                the error which the parameter does not meet the requirement.
        """
        checkedList = []
        for typeWant, handle in typeWantAndHandle:
            checkedList.append(f'{typeWant}')
            if type(target) == typeWant:
                handle = (lambda x: x) if handle == None else handle
                return handle(target)

        raise TypeError(
            'Expected'.join([f"'{typeWant}', " for typeWant, _ in checkedList[:-1]]) +
            f"or '{checkedList[-1]}', but got '{type(target)}'. "
        )

    def make(
        self,
        inputObject: dict[any] = {},
        partial: list[any] = [],
    ) -> dict[any]:
        """Export a dictionary of configuration.

        Args:
            inputObject (dict[any], optional): Additonal object. Defaults to `{}`.

        Returns:
            dict[any]: A dictionary of configuration.
        """

        configIndividual = {
            **self.default,
            **inputObject,
        }

        if len(partial) == 0:
            return configIndividual
        else:

            return {k: configIndividual[k] for k in partial if k in configIndividual}

    def json_make(
        self,
        inputObject: dict[any] = {},
        partial: list[any] = [],
    ) -> dict[any]:
        """Export a dictionary of configuration which is jsonable.

        Args:
            inputObject (dict[any], optional): Additonal object. Defaults to {}.

        Returns:
            dict[any]: A dictionary of configuration.
        """

        return jsonablize(self.make(
            inputObject=inputObject,
            partial=partial,
        ))

    def _handleInput(
        self,
        inputObject: Optional[dict[any]] = None
    ) -> None:
        """Check the input for :meth:`.check` and :meth:`.ready`.

        Args:
            inputObject (Optional[dict[any]], optional): 
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

    def check(
        self,
        target: Optional[dict[any]] = None,
        ignores: list[str] = [],
    ) -> list:
        """Check whether the configuration is completed.

        Args:
            target (dict): The configuration.

        Returns:
            list: The lost keys of the configuration.
        """
        self._handleInput(target)
        return [k for k in self.default if not (k in target or k in ignores)]

    def ready(
        self,
        target: dict = {},
        ignores: list[str] = [],
    ) -> bool:
        """Check whether the configuration is completed.

        Args:
            target (dict): The configuration

        Returns:
            bool: Whether the configuration is completed
        """
        self._handleInput(target)
        return all(k in target or k in ignores for k in self.default)

    def __repr__(self):
        return f"{self.__name__}({self.__dict__})"

    def jsonize(self):
        return jsonablize(self.__dict__)
    
    
class defaultConfig():
    __version__ = (0, 1, 0)
    def __init__(
        self,
        default: dict[str, any] = {},
        name: str = "defaultConfig",
        default_names: Iterable[str] = [],
    ) -> None:
        """Set the default parameters dictionary for multiple experiment.

        A replacement of :cls:`Configuration`.

        Args:
            default (Optional[dict[any]], optional): [description]. Defaults to None.
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
    
    def __getitem__(self, key) -> any:
        return self.default[key]
        
    def __iter__(self):
        for k, v in self.default.items():
            yield k, v
        
    def _handleInput(
        self,
        inputObject: Optional[dict[any]] = None
    ) -> None:
        """Check the input for :meth:`.check` and :meth:`.ready`.

        Args:
            inputObject (Optional[dict[any]], optional): 
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
        __values: dict[str, any] = {},
        partial: list[str] = [],
    ) -> dict[str, any]:
        """Export a dictionary of configuration.

        Args:
            __values (dict[str, any], optional): Additonal object. Defaults to `{}`.
            partial (list[str], optional): Export parts of configuration. Defaults to `[]` as exporting all.

        Returns:
            dict[str, any]: A dictionary of configuration.
        """
        
        exportDict = {
            **self.default,
            **__values,
        }
        if len(partial) == 0:
            return exportDict
        else:
            return {
                k: v for k, v in exportDict.items()
                if k in partial
            }
            
    def json_make(
        self,
        __values: dict[str, any] = {},
        partial: list[any] = [],
    ) -> dict[any]:
        """Export a dictionary of configuration which is jsonable.

        Args:
            inputObject (dict[any], optional): Additonal object. Defaults to {}.

        Returns:
            dict[any]: A dictionary of configuration.
        """

        return jsonablize(self.make(
            __values=__values,
            partial=partial,
        ))
        
    def namedtuple(
        self,
        __values: dict[str, any] = {},
    ) -> NamedTuple:
        """Export configuration as a namedtuple.

        Args:
            __values (dict[str, any], optional): _description_. Defaults to {}.

        Returns:
            _type_: _description_
        """    

        return self.namedtupleType(**__values)
    
    def check(
        self,
        target: Optional[dict[any]] = None,
        ignores: list[str] = [],
    ) -> list:
        """Check whether the configuration is completed.

        Args:
            target (dict): The configuration.

        Returns:
            list: The lost keys of the configuration.
        """
        self._handleInput(target)
        return [k for k in self.namedtupleType._fields if not (k in target or k in ignores)]

    def ready(
        self,
        target: dict = {},
        ignores: list[str] = [],
    ) -> bool:
        """Check whether the configuration is completed.

        Args:
            target (dict): The configuration

        Returns:
            bool: Whether the configuration is completed
        """
        self._handleInput(target)
        return all(k in target or k in ignores for k in self.namedtupleType._fields)
    
    def contain(
        self,
        target: dict = {},
        ignores: list[str] = [],
    ) -> bool:
        """Check whether the configuration contains some key of completed one.

        Args:
            target (dict): The configuration

        Returns:
            bool: Whether the configuration is completed
        """
        self._handleInput(target)
        for k in self.namedtupleType._fields:
            if (k in target or k in ignores):
                return True
            
        return False
        
    def has(
        self,
        target: dict = {},
        ignores: list[str] = [],
        reverse: bool = False,
    ) -> bool:
        """Check whether the configuration contains what keys of completed one.

        Args:
            target (dict): The configuration

        Returns:
            list: The contained keys of the configuration.
        """
        self._handleInput(target)
        keylist = []
        nokeylist = []
        for k in self.namedtupleType._fields:
            if (k in target or k in ignores):
                keylist.append(k)
            else:
                nokeylist.append(k)
            
        if reverse:
            return nokeylist
        else:
            return keylist
    
    def __repr__(self):
        return f"{self.namedtupleType()}"

    