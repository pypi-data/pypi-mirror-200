"""
Module defines the :class:`.BetterDict` class.

The :class:`.BetterDict` class is a subclass of the :class:`dict` class that
provides additional functionality to the dictionary. The additional
functionality includes:

- Accessing the dictionary keys by value.
- Manipulating the dictionary keys and values using index notation.
- Accessing and manipulating the dictionary values using dot notation.
- Accessing the dictionary values by their data types.
- Saving and loading the dictionary to and from a file.
- Creating the dictionary from a :class:`pandas.DataFrame` object.
- Creating the dictionary from a :class:`numpy.ndarray` object.
- Creating the dictionary from a :class:`numpy.matrix` object.
- Creating the dictionary from a :class:`pandas.Series` object.
- Applying a function to the dictionary values and keys.
- Finding keys using fuzzy matching.
- Renaming the dictionary keys.

"""
from __future__ import annotations

from abc import abstractmethod
from difflib import get_close_matches
from typing import Any, Hashable, Iterable, List, Tuple

import numpy as np
import pandas as pd

from better_dict.accessors import ILoc, VLoc
from better_dict.io import JoblibIOMixin, PicklerMixin
from better_dict.utils import (flatten, iterable_not_string, make_list,
                               same_length)


def translate_dtype(dtype: str) -> type | Tuple[type, ...]:
    """Translate the ``dtype`` string to the corresponding Python type.

    Parameters
    ----------
    dtype : str
        Data type represented as string to translate.

    Returns
    -------
    type | Tuple[type, ...]
        Type or tuple of types corresponding to the text data types.

    Raises
    ------
    ValueError
        If the data type string is not recognized.
    """
    if dtype == "number":
        return float, int
    if dtype == "string":
        return str
    if dtype == "datetime":
        return pd.Timestamp
    if dtype == "pandas":
        return pd.DataFrame, pd.Series
    if dtype == "numpy":
        return np.ndarray, np.matrix
    raise ValueError(f"Invalid dtype: {dtype!r}")


class ApplyMixin:
    """
    Mixin class that adds the apply method to the ``BetterDict`` class.

    The ``apply`` method enables operations on the values or keys of the
    dictionary.

    """

    @abstractmethod
    def rename(self, keys: dict) -> None:
        """Rename the keys of the dictionary."""

    @abstractmethod
    def keys(self):
        """Get the keys of the dictionary."""

    @abstractmethod
    def values(self):
        """Get the values of the dictionary."""

    @abstractmethod
    def __setitem__(self, key, value):
        """Set the value of the dictionary at the given key."""

    def apply(self, func, *args, axis=1, **kwargs):
        """Apply a function to the ``BetterDict`` keys or values.

        Parameters
        ----------
        func : callable
            Function to apply.
        *args
            Positional arguments to pass to the function.
        **kwargs
            Keyword arguments to pass to the function.
        axis : int, default 1
            Axis along which to apply the function. If ``axis=0``, the function
            is applied to the keys of the dictionary. If ``axis=1``, the
            function is applied to the values of the dictionary.

        Returns
        -------
        BetterDict
            Result of applying the function to the object.

        Notes
        -----
        The class mimics the ``pandas.DataFrame.apply`` method.
        """
        if axis == 1:
            return self.value_apply(func, *args, **kwargs)
        return self.keys_apply(func, *args, **kwargs)

    def keys_apply(self, func, *args, **kwargs):
        """Apply the function to the keys of the dictionary.

        Parameters
        ----------
        func : callable
            Function to apply.
        *args
            Positional arguments to pass to the function.
        **kwargs
            Keyword arguments to pass to the function.

        Returns
        -------
        BetterDict
            Result of applying the function to the keys of the object.
        """
        self.rename({key: func(key, *args, **kwargs) for key in self.keys()})
        return self

    def value_apply(self, func, *args, **kwargs):
        """Apply the function to each value of a dictionary.

        Parameters
        ----------
        func : callable
            Function to apply.
        *args
            Positional arguments to pass to the function.
        **kwargs
            Keyword arguments to pass to the function.

        Returns
        -------
        BetterDict
            Result of applying the function to each row of the object.
        """
        new_values = (func(value, *args, **kwargs) for value in self.values())
        for key, value in zip(self.keys(), new_values):
            self[key] = value
        return self


class BetterDict(dict, PicklerMixin, JoblibIOMixin, ApplyMixin):
    """
    Custom dictionary class that allows multiple get/set operations at once.

    Class also supports the following operations:

    - Access and set values using index notation.
    - Access keys referrencing the dictionary values.
    - Get the keys and values as lists.
    - Get the closest match to a given key.
    - Select a subset of the dictionary based on the values data types.
    - Apply functions row- and column-wise.
    - Perform I/O operations using ``pickle`` and ``joblib``.

    Examples
    --------
    Create a :class:`.BetterDict` instance from a normal dictionary:
    >>> d = BetterDict({"a": 1, "b": 2})
    >>> d["a"]
    1

    Get multiple values at once
    >>> d["a", "b"]
    {'a': 1, 'b': 2}

    Set multiple values at once
    >>> d["a", "b"] = 3, 4
    >>> d["a", "b"]
    {'a': 3, 'b': 4}

    Access values using index notation
    >>> d.iloc[0]
    3

    Set values using index notation
    >>> d.iloc[0, 1] = [5, 6]
    >>> d.iloc[:]
    [5, 6]

    Get the keys and values as lists
    >>> d.keys()    # Dictionary keys
    ['a', 'b']
    >>> d.values()  # Dictionary values
    [5, 6]

    Get the closest match to a given key
    >>> d.get_closest_match("A")
    'a'

    """

    @property
    def iloc(self) -> ILoc:
        """Access the dictionary values by index.

        Returns
        -------
        ILoc
            Dictionary values accessed by index.
        """
        return ILoc(self)

    @property
    def vloc(self) -> VLoc:
        """Access the dictionary values by value.

        Returns
        -------
        VLoc
            Dictionary values accessed by value.
        """
        return VLoc(self)

    @property
    def index(self) -> List[int]:
        """Get the indexes of the dictionary.

        Returns
        -------
        List[int]
            Indexes of the dictionary.
        """
        return self.iloc.index

    def __getitem__(
        self, key: Hashable | Iterable[Hashable],
    ) -> object | BetterDict:
        """Get the value(s) associated with the key(s).

        Parameters
        ----------
        key : Hashable | Iterable[Hashable]
            Key(s) to get the value(s) for.

        Returns
        -------
        object | BetterDict
            Value(s) associated with the key(s).
        """
        if iterable_not_string(key):
            return BetterDict({_key: self[_key] for _key in key})
        return self.get(key)

    def __setitem__(
        self, key: Hashable | Iterable[Hashable], value: Any | Iterable[Any],
    ):
        """Set the value(s) associated with the key(s).

        Parameters
        ----------
        key : Hashable | Iterable[Hashable]
            Key(s) to set the value(s) for.
        value : Any | Iterable[Any]
            Value(s) to set.
        """
        if same_length(key, value):
            for _key, _value in zip(key, value):
                super().__setitem__(_key, _value)
        else:
            super().__setitem__(key, value)

    def __getattr__(self, name: str) -> object:
        """Get the value associated with the key.

        Parameters
        ----------
        name : str
            Key to get the value for.

        Returns
        -------
        object
            Value associated with the key.
        """
        return self.__getitem__(name)

    def __setattr__(self, name: str, value: Any):
        """Set the value associated with the key.

        Parameters
        ----------
        name : str
            Key to set the value for.
        value : Any
            Value to set.
        """
        self.__setitem__(name, value)

    def rename(self, keys):
        """Rename the keys of the dictionary.

        Parameters
        ----------
        keys : dict
            New keys for the dictionary.
        """
        new_keys = keys.values()
        old_keys = keys.keys()
        for old_key, new_key in zip(old_keys, new_keys):
            value = self.pop(old_key)
            self[new_key] = value

    def keys(self) -> List[Hashable]:
        """Return a list of the dictionary keys.

        Returns
        -------
        List[Hashable]
            List of the dictionary keys.
        """
        return list(super().keys())

    def values(self) -> List[Any]:
        """Return a list of the dictionary values.

        Returns
        -------
        List[Any]
            List of the dictionary values.
        """
        return list(super().values())

    def close_match(self, key: Hashable, cutoff: float = 0.6) -> Hashable:
        """
        Return the key that is the closest match to the name from ``key``.

        Before applying the fuzzy match, the ``key`` and the dictionary
        keys are converted to lower case. This maximizes the chances of
        finding a match.

        Parameters
        ----------
        key : Hashable
            Key to find the closest match for.
        cutoff : float, default 0.6
            Minimum similarity ratio for a match to be returned. The parameter
            must be between 0 and 1. A value of 1 means that the strings must
            be identical. A value close to 0 means that the strings don't have
            to be identical, for a match to be returned.

        Returns
        -------
        Hashable
            Closest match to the given key.

        Raises
        ------
        KeyError
            If no match is found.
        """
        lower_keys = BetterDict(
            {str(_key).lower(): _key for _key in self.keys()}
        )
        lower_key = str(key).lower()
        matches = get_close_matches(  # type: ignore
            lower_key, lower_keys.keys(), cutoff=cutoff
        )
        if matches:
            return lower_keys[matches[0]]
        raise KeyError(f"No close match found for {key}.")

    def dtypes(self) -> BetterDict:
        """Get the data types of the dictionary values.

        Returns
        -------
        BetterDict
            Data types of the dictionary values.
        """
        return BetterDict({key: type(value) for key, value in self.items()})

    def select_dtypes(self, include=None, exclude=None):
        """
        Return a subset of the dictionary based on the data types.

        At least one of ``include`` or ``exclude`` must be specified and if
        both are specified, ``include`` cannot contain the same data types as
        ``exclude``.

        This function accepts some special strings to specify the data types:

        - ``'number'`` - Numeric data types.
        - ``'string'`` - String data types.
        - ``'pandas'`` - Pandas DataFrame or Series.
        - ``'numpy'`` - Numpy array.
        - ``'datetime'`` - Datetime data types.

        Parameters
        ----------
        include : list, default None
            Data types to include in the subset. If ``exclude`` is not
            specified, then this parameter is obligatory.
        exclude : list, default None
            Data types to exclude from the subset. If ``include`` is not
            specified, then this parameter is obligatory.

        Returns
        -------
        BetterDict
            Subset of the dictionary based on the data types.

        Raises
        ------
        ValueError
            - If both ``include`` and ``exclude`` are not specified.
            - If ``include`` contains the same data types as ``exclude``.

        Examples
        --------
        >>> from better_dict import BetterDict
        >>> d = BetterDict({'a': 1, 'b': '2', 'c': [3], 'd': {'e': 4}})
        >>> d.select_dtypes(include=['number', 'string'])
        BetterDict({'a': 1, 'b': '2'})

        Notes
        -----
        Method checks whether at least one of ``include`` or ``exclude`` is
        specified and if both are specified, it checks whether ``include``
        contains the same data types as ``exclude``. If any of these checks
        fail, a ``ValueError`` is raised.

        This method works similarly to the ``pandas.DataFrame.select_dtypes``
        method.

        See Also
        --------
        - :meth:`pandas.DataFrame.select_dtypes`
        - :func:`.translate_dtype`
        - :func:`better_dict.utils.make_list`
        - :func:`better_dict.utils.flatten`
        """
        if include is None and exclude is None:
            raise ValueError(
                "At least one of ``include`` or ``exclude`` must be specified."
            )
        include = tuple(
            flatten(
                [
                    translate_dtype(dtype) if isinstance(dtype, str) else dtype
                    for dtype in make_list(include)
                ]
            )
        )
        exclude_dtypes = tuple(
            flatten(
                [
                    translate_dtype(dtype) if isinstance(dtype, str) else dtype
                    for dtype in make_list(exclude)
                ]
            )
        )
        check_include_exclude = set(include).intersection(set(exclude_dtypes))
        if check_include_exclude:
            raise ValueError(
                "Cannot set the same data types to `include` and `exclude`:\n"
                "\n".join(f"- {dtype}" for dtype in check_include_exclude)
            )
        return BetterDict(
            {
                key: value
                for key, value in self.items()
                if isinstance(value, include)
                and not isinstance(value, exclude_dtypes)
            }
        )

    @classmethod
    def from_frame(cls, pandas_df: pd.DataFrame) -> BetterDict:
        """Create a ``BetterDict`` from a pandas DataFrame.

        Parameters
        ----------
        pandas_df : pd.DataFrame
            Pandas DataFrame to create the ``BetterDict`` from.

        Returns
        -------
        BetterDict
            ``BetterDict`` created from the pandas DataFrame.
        """
        return cls(pandas_df.to_dict(orient="list"))

    @classmethod
    def from_series(cls, pandas_series: pd.Series) -> BetterDict:
        """Create a ``BetterDict`` from a pandas Series.

        Parameters
        ----------
        pandas_series : pd.Series
            Pandas Series to create the ``BetterDict`` from.

        Returns
        -------
        BetterDict
            ``BetterDict`` created from the pandas Series.
        """
        return cls(pandas_series.to_dict())

    @classmethod
    def from_list(cls, list_obj: list) -> BetterDict:
        """Create a ``BetterDict`` from a list.

        Parameters
        ----------
        list_obj : list
            List to create the ``BetterDict`` from.

        Returns
        -------
        BetterDict
            ``BetterDict`` created from the list.
        """
        return cls(enumerate(list_obj))
