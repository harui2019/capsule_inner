from .jsonablize import Parse as jsonablize
from typing import NamedTuple, Iterable
from collections import namedtuple
import warnings


class argdict(dict):
    __name__ = 'argdict'
    __version__ = (0, 2, 0)

    def __init__(
        self,
        params: dict[any],
        paramsKey: list[str] = [],
    ) -> None:
        """This class is a container to keep the parameters for each experiment.
        And it's also an inherition of `dict`.

        In future, with the rebuilding of :meth:`multiOuput`, :meth:`powerOutput`
        :cls:`argdict` will replace by :cls:`argTuple`, a better data structure made by :cls:`namedtuple`.

        - :cls:`NameTuple` of :module:`typing` can be the type hint for this class.

        ## example:

        >>> A = argset({'a': 22})

        - call

        >>> A['a'], A.a
        `('22', '22')`

        - iterations

        >>> [k for k in A]
        `['a']`

        - keys

        >>> ('a' in A)
        `True`

        - iterable unpacking

        >>> {**A}
        `{'a': 22}`

        Args:
            params (dict[str, any]): The parameters of the experiment.
            paramsKey (list[str]): The necessary parameters of the experiment.
        """

        super().__init__(params)
        blacklist = dir({})

        for k in paramsKey:
            if k in blacklist:
                warnings.warn(
                    f"'{k}' will be not added as attribution but can be called by subscript" +
                    "due to this attribution is used for class working.")
            else:
                self.__setattr__(k, None)
        for k in params:
            if k in blacklist:
                warnings.warn(
                    f"'{k}' will be not added as attribution but can be called by subscript" +
                    "due to this attribution is used for class working.")
            else:
                self.__setattr__(k, params[k])

    def __getitem__(self, key) -> any:
        return self.__dict__[key]

    def __setitem__(self, key, value) -> None: ...

    def to_dict(self) -> dict[str, any]:
        return self.__dict__

    def __iter__(self):
        for k, v in self.__dict__.items():
            yield k, v

    def jsonize(self) -> dict[str, str]:
        return jsonablize(self.__dict__)

    def __repr__(self) -> str:
        return f'{self.__name__}({self.__dict__})'


class attributedDict:
    __name__ = "attributedDict"
    __version__ = (0, 0, 1)
    
    def __init__(
        self,
        field: dict[str, any] = {},
        name: str = "attributedDict",
        field_names: Iterable[str] = [],
        **otherArgs,
    ) -> None:
        """This class is a container to keep the parameters for each experiment.
        And it's also an inherition of `dict`.

        A replacement of :cls:`argdict`.
        

        - :cls:`NameTuple` of :module:`typing` can be the type hint for this class.

        ## example:

        >>> A = argset({'a': 22})

        - call

        >>> A['a'], A.a
        `('22', '22')`

        - iterations

        >>> [k for k in A]
        `['a']`

        - keys

        >>> ('a' in A)
        `True`

        - iterable unpacking

        >>> {**A}
        `{'a': 22}`

        Args:
            field (dict[str, any]): The parameters of the experiment.
            field_names (Iterable[str]): The necessary parameters of the experiment.
        """

        # downward compatibility for :cls:argdict
        
        self.__name__ = name
        
        self._saveDict = {}
        if 'params' in otherArgs and len(field) == 0:
            field = otherArgs['params']
            
        if 'paramsKey' in otherArgs and len(field_names) == 0:
            field = otherArgs['paramsKey']
            
        for k in field_names:
            self._setitem_check(k)
            self._saveDict[k] = None
            self.__setattr__(k, self._saveDict[k])
            
        for k in field:
            self._setitem_check(k)
            self._saveDict[k] = field[k]
            self.__setattr__(k, self._saveDict[k])
            
        for k in dir(self._saveDict):
            if k[:2] != '__':
                self.__setattr__('_'+k, self._saveDict.__getattribute__(k))
            
    def __getitem__(self, key) -> any:
        return self._saveDict[key]
    
    @staticmethod
    def _setitem_check(__name) -> None:
        if __name.startswith('_'):
            raise ValueError(f"Field names cannot start with an underscore: '{__name!r}'")
    
    def __setitem__(self, key, value) -> None:
        self._setitem_check(key)
        self._saveDict[key] = value
        self.__setattr__(key, self._saveDict[key])
        
    def __iter__(self):
        for k, v in self._saveDict.items():
            yield k, v
            
    def _asdict(self) -> dict[str, any]:
        return self._saveDict
    
    def _jsonize(self) -> dict[str, any]:
        return jsonablize(self._saveDict)
    
    def __repr__(self) -> str:
        return f'{self.__name__}({self._saveDict})'
    

def argTuple(
    params: dict[str, any],
    paramsKey: list[str] = [],
    name: str = 'argTuple',
) -> NamedTuple:
    """This class is a container to keep the parameters for each experiment powered by :cls:`NamedTuple`.

    - :cls:`NameTuple` of :module:`typing` can be the type hint for this class.
    Deprecated.

    ## example:

    >>> A = argset({'a': 22})

    - call

    >>> A['a'], A.a
    `('22', '22')`

    - iterations

    >>> [k for k in A]
    `['22']`

    - keys

    >>> ('a' in A)
    `True`

    - iterable unpacking

    >>> {**A}
    `{'a': 22}`

    Args:
        params (dict[str, any]): The parameters of the experiment.
        paramsKey (list[str]): The necessary parameters of the experiment.
    """

    f = {
        **{k: None for k in paramsKey},
        **{k: v for k, v in params.items()},
    }
    prototype = namedtuple(field_names=f.keys(), typename=name)

    class argTuple(prototype):
        def __getitem__(self, key) -> any:
            try:
                return self.__getattribute__(key)
            except AttributeError as e:
                raise KeyError(e, ', so this key is not in the argTuple.')

        def keys(self) -> list:
            return self._fields

        def jsonize(self) -> dict[str, str]:
            return jsonablize(self._asdict())

    return argTuple(**f)
