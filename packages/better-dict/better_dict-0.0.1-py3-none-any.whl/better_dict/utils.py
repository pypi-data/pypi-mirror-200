"""
Module defines helper functions for the ``better_dict`` package.

Functions
---------
- :func:`.iterable_not_string`: Check if the value is iterable but not a string.
- :func:`.same_length`: Check if the keys and values have the same length.
- :func:`.make_list`: Make a list from the value.
- :func:`.flatten`: Flatten the iterable object.

"""
from __future__ import annotations

from typing import Any, Generator, Iterable, List


__all__ = [
    "flatten",
    "iterable_not_string",
    "make_list",
    "same_length",
]


def iterable_not_string(value: object) -> bool:
    """Check if the value is iterable but not a string.

    Parameters
    ----------
    value : object
        Value to check.

    Returns
    -------
    bool
        ``True`` if the value is iterable but not a string, ``False`` otherwise.

    Examples
    --------
    >>> iterable_not_string([1, 2, 3])
    True
    >>> iterable_not_string('abc')
    False
    >>> iterable_not_string(1)
    False
    """
    return isinstance(value, Iterable) and not isinstance(value, str)


def same_length(keys: Any, values: Any) -> bool:
    """Check if the keys and values have the same length.

    Parameters
    ----------
    keys : Any
        Keys to check.
    values : Any
        Values to check.

    Returns
    -------
    bool
        True if the keys and values are iterables and have the same length,
        False otherwise.

    Examples
    --------
    >>> same_length([1, 2, 3], [4, 5, 6])
    True
    >>> same_length([1, 2, 3], [4, 5])
    False
    >>> same_length([1, 2, 3], 4)
    False
    """
    if all(
        iterable_not_string(value) and hasattr(value, "__len__")
        for value in [keys, values]
    ):
        return len(keys) == len(values)
    return False


def make_list(value: Any) -> List[Any]:
    """Make a list from the value.

    Parameters
    ----------
    value : Any
        Value to make a list from.

    Returns
    -------
    List[Any]
        List with the value.
    """
    if value is None:
        return []
    return list(value) if iterable_not_string(value) else [value]


def flatten(line: Any) -> Generator:
    """Flatten an arbitrarily nested sequence.

    Parameters
    ----------
    line : Any
        The possibly nested sequence to flatten.

    Returns
    -------
    flattened : generator
        A generator that yields the flattened sequence.

    Examples
    --------
    >>> list(flatten([[1, 2, 3], 4, [5, [6, 7, 8]]]))
    [1, 2, 3, 4, 5, 6, 7, 8]
    >>> list(flatten(1))
    [1]

    Notes
    -----
    - This function doesn't consider strings sequences.
    - If the input is not a sequence, it is returned as a single element list.
    """
    for element in make_list(line):
        if iterable_not_string(element):
            yield from flatten(element)
        else:
            yield element
