"""
Accessor classes for :class:`better_dict.core.BetterDict` dictionary.

Classes
-------
This module defines the following classes:

- :class:`.VLoc`: Class allows the key retrieval using the dictionary values.
- :class:`.ILoc`: Class allows access and setting values using index notation.

Notes
-----
The :class:`.VLoc` and :class:`.ILoc` classes can be used by any dictionary-like
class. To create a new class that inherits from :class:`.VLoc` or :class:`.ILoc`
you must define the following properties:

- ``iloc``: property needed to implement the :class:`.ILoc` class.
- ``vloc``: property needed to implement the :class:`.VLoc` class.

The following example shows how to implement them:

.. code-block:: python

    class MyDict(dict, VLoc, ILoc):
        @property
        def iloc(self):
            return ILoc(self)

        @property
        def vloc(self):
            return VLoc(self)

In the example above, the ``MyDict`` class inherits from the ``dict``,
:class:`.ILoc` and :class:`.VLoc` classes. By defining the properties
``iloc`` and ``vloc`` and passing ``self`` to the :class:`.ILoc` and
:class:`.VLoc`, the dictionary keys and values can be accessed by the
:class:`.ILoc` and :class:`.VLoc` classes.

"""
from __future__ import annotations

from typing import Any, Hashable, Iterable, List

import numpy as np

from better_dict.utils import (iterable_not_string, same_length)


class VLoc:
    """
    Class for accessing the keys of a dictionary by value.

    Parameters
    ----------
    data : BetterDict
        Dictionary to access.

    Examples
    --------
    The following example shows how to use the :class:`.VLoc` class to access
    the keys of a dictionary by value.
    >>> from better_dict import BetterDict
    >>> d = BetterDict({'a': 1, 'b': 2, 'c': 3})
    >>> d.vloc[1]
    ['a']

    Notes
    -----
    The :class:`.VLoc` class only allows access to the keys of the dictionary
    by value. It does not allow manipulations of the dictionary keys or values.

    """

    def __init__(self, data):
        self.data = data

    def __getitem__(self, value: object | Iterable[object]) -> List[Hashable]:
        """Get the keys of the dictionary that match the value(s).

        Parameters
        ----------
        value : object | Iterable[object]
            Value(s) to match.

        Returns
        -------
        List[Hashable]
            keys(s) of the dictionary that match the value(s).
        """
        if not isinstance(value, (np.ndarray, list, tuple, set)):
            value = [value]
        return [_key for _key, _value in self.data.items() if
                any(v == _value for v in value)]

    def inverse(self):
        """Get the inverse of the dictionary.

        Returns
        -------
        BetterDict
            Inverse of the dictionary.
        """
        return self.data.__class__(
            {value: key for key, value in self.data.items()}
        )


class ILoc:
    """
    Class for manipulating :class:`.BetterDict` using index notation.

    Parameters
    ----------
    data : BetterDict
        Dictionary to access as a :class:`.BetterDict` object.

    Methods
    -------
    __getitem__(index: int | Iterable[int]) -> Any
        Get the value of the dictionary at the given index(es).
    __setitem__(index: int | Iterable[int], value: Any | Iterable[Any]) -> None
        Set the value(s) of the dictionary at the given index(es).

    Attributes
    ----------
    data : BetterDict
        Dictionary to access as a :class:`.BetterDict` object.

    Examples
    --------
    The following example shows how to use the :class:`.ILoc` class to access
    the values of a :class:`.BetterDict` dictionary using index notation:
    >>> from better_dict import BetterDict
    >>> d = BetterDict({'a': 1, 'b': 2, 'c': 3})
    >>> d.iloc[0]
    1

    You can also use the :class:`.ILoc` class get multiple values at once:
    >>> d.iloc[0, 1]
    [1, 2]
    >>> d.iloc[[0, 1]]
    [1, 2]
    >>> d.iloc[1:]
    [2, 3]

    Class allows setting multiple values at once using index notation:
    >>> d.iloc[[0, 1]] = [10, 20]
    >>> d
    {'a': 10, 'b': 20, 'c': 3}

    """

    def __init__(self, data):
        self.data = data

    def __getitem__(self, index: int | Iterable[int]) -> Any:
        """Get the value of the dictionary at the given index(es).

        Parameters
        ----------
        index : int | Iterable[int]
            Index(es) of the value(s) to get.

        Returns
        -------
        Any
            Value(s) of the dictionary at the given index(es).
        """
        values = list(self.data.values())
        return (
            [values[i] for i in index] if iterable_not_string(index)
            else values[index]
        )

    def __setitem__(
        self, index: int | Iterable[int], value: Any | Iterable[Any],
    ) -> None:
        """
        Set the value(s) of the dictionary at the given index(es).

        To set multiple values at once, you need to specify the same number of
        indices and values, for example:

        .. code-block:: python

            d.iloc[[0, 1]] = [10, 20]

        Parameters
        ----------
        index : int | Iterable[int]
            Index(es) of the value(s) to set.
        value : Any | Iterable[Any]
            Value(s) to set.

        """
        keys = list(self.data.keys())
        if same_length(index, value):
            for _index, _value in zip(index, value):
                self.data[keys[_index]] = _value
        else:
            self.data[keys[index]] = value

    @property
    def index(self) -> List[int]:
        """Get the indexes of the dictionary.

        Returns
        -------
        List[int]
            Indexes of the dictionary.
        """
        return list(range(len(self.data.keys())))
