"""
Module contains classes that allow performing I/O operations on objects.

This module defines classes that serve as mixins for other classes.
These classes extensions inject methods that allow performing I/O
operations on objects.

Classes
-------
This module defines the following classes:

- :class:`.PicklerMixin`: Mixin class that adds methods for pickling objects.
- :class:`.JoblibIOMixin`: Mixin class that adds methods for saving objects as
  joblib files.

Examples
--------
The following example shows how to use the :class:`.PicklerMixin` class to
extend other classes, adding methods for pickling objects:

.. code-block:: python

    class MyClass(PicklerMixin):pass

    my_object = MyClass()
    # Save classe instance as pickle file
    my_object.to_pickle('my_object.pkl')

    # Load class instance from pickle file
    MyClass.from_pickle('my_object.pkl')

The same logic applies to the :class:`.JoblibIOMixin` class.

Notes
-----
All I/O classes from this module implement the saving method, using the ``to_``
prefix, and the loading method, using the ``from_`` prefix.
The loading methods are class methods, so they can be called directly from the
class, without the need to instantiate it first.
"""
from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any, Dict

import joblib


class PicklerMixin:
    """
    Mixin class for pickle I/O.

    This class allows parent objects to perform I/O operations using pickle.
    The methods implemented in this class are:

    - :meth:`.PicklerMixin.to_pickle`: Save the object to a pickle file.
    - :meth:`.PicklerMixin.from_pickle`: Load the object from a pickle file.

    Examples
    --------
    >>> class MyClass(PicklerMixin):pass
    >>> obj = MyClass()

    >>> # To save the object to a pickle file:
    >>> obj.to_pickle("path/to/file")

    >>> # To load the object from a pickle file:
    >>> obj.from_pickle("path/to/file")

    """

    def __getstate__(self) -> Dict[str, Any]:
        """Get the state of the object for pickling.

        Returns
        -------
        Dict[str, Any]
            State of the object for pickling.
        """
        return self.__dict__

    def __setstate__(self, state: Dict[str, Any]):
        """Set the state of the object after unpickling.

        Parameters
        ----------
        state : Dict[str, Any]
            State of the object after unpickling.
        """
        self.__dict__ = state

    def to_pickle(self, path: str):
        """Save the object to a pickle file.

        Parameters
        ----------
        path : str
            Path to the pickle file.

        Raises
        ------
        ValueError
            If the path refers to a directory.
        """
        _path = Path(path).with_suffix(".pickle")
        if _path.is_dir():
            raise ValueError(f"{path!r} is a directory.")
        with open(_path, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def from_pickle(cls, path: str) -> PicklerMixin:
        """Load the object from a pickle file.

        Parameters
        ----------
        path : str
            Path to the pickle file.

        Returns
        -------
        PicklerMixin
            Object loaded from the pickle file.

        Raises
        ------
        ValueError
            If the path is not a file.
        """
        _path = Path(path).with_suffix(".pickle")
        if not _path.is_file():
            raise ValueError(f"{path!r} is not a file.")
        with open(_path, "rb") as file:
            # codiga-disable
            return cls(pickle.load(file))  # noqa


class JoblibIOMixin:
    """
    Mixin class for joblib I/O.

    This class allows parent objects to perform I/O operations using ``joblib``.
    The methods implemented in this class are:

    - :meth:`.JoblibIOMixin.to_joblib`: Save the object to a joblib file.
    - :meth:`.JoblibIOMixin.from_joblib`: Load the object from a joblib file.

    Methods
    -------
    to_joblib(path: str)
        Save the object to a joblib file.
    from_joblib(path: str)
        Load the object from a joblib file.

    Examples
    --------
    Define a class that inherits from :class:`.JoblibIOMixin`:
    >>> class MyClass(JoblibIOMixin):pass
    >>> obj = MyClass()

    Save the object as a ``joblib`` file:
    >>> obj.to_joblib("path/to/file")

    Load the object from a ``joblib`` file:
    >>> obj.from_joblib("path/to/file")

    """

    def to_joblib(self, path: str) -> None:
        """Save the object to a ``joblib`` file.

        Parameters
        ----------
        path : str
            Path to the ``joblib`` file.

        Raises
        ------
        ValueError
            If the path refers to a directory.
        """
        _path = Path(path).with_suffix(".joblib")
        if _path.is_dir():
            raise ValueError(f"{path!r} is a directory.")
        joblib.dump(self, _path)

    @classmethod
    def from_joblib(cls, path: str) -> JoblibIOMixin:
        """Load the object from a ``joblib`` file.

        Parameters
        ----------
        path : str
            Path to the ``joblib`` file.

        Returns
        -------
        JoblibIOMixin
            Object loaded from the ``joblib`` file.

        Raises
        ------
        ValueError
            If the path is not a file.
        """
        _path = Path(path).with_suffix(".joblib")
        if not _path.is_file():
            raise ValueError(f"{path!r} is not a file.")
        return cls(joblib.load(_path))  # noqa
