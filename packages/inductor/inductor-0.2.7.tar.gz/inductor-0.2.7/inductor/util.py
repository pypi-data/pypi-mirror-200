# Copyright 2022 Inductor, Inc.

"""Utility functionality."""

import os
import threading
from typing import Callable, Iterable, Union


class UniqueIdGen:
    """A unique ID generator."""

    def __init__(self, id_prefix: str = ""):
        """Constructs a new UniqueIdGen.

        Args:
            id_prefix: Prefix for all IDs produced by this instance.
        """
        self._id_prefix = id_prefix
        self._lock = threading.Lock()
        self._index = 0

    def unique_id(self, count: int = 1) -> Union[str, Iterable[str]]:
        """Returns strings that are unique across all calls on this instance.

        Args:
            count: Number of unique strings to return.

        Returns:
            A single unique string if count == 1; otherwise, an iterable of
            unique strings.  All returned strings start with id_prefix and
            otherwise contain only characters in {a-z, A-Z, 0-9, _}.  Every
            string returned is guaranteed to never before have been returned
            by a call to this method on the same UniqueIdGen instance.
        """
        with self._lock:
            index_start = self._index
            self._index += count
        if count == 1:
            return f"{self._id_prefix}_{index_start}"
        else:
            return [
                f"{self._id_prefix}_{i}"
                for i in range(index_start, index_start + count)]

    def fork(self) -> "UniqueIdGen":
        """Returns a new UniqueIdGen derived from this instance.

        Strings produced by the returned UniqueIdGen's unique_id() method are
        guaranteed to start with id_prefix and to be unique across all IDs
        produced by this instance and any instances descended from it via
        any number of successive fork() calls on this instance or its
        forked descendants.
        """
        return UniqueIdGen(self.unique_id())


def module_qualname(f: Callable) -> str:
    """Returns the fully qualified name of the module in which f is defined.

    Args:
        f: A function, class, or method.

    Returns:
        The fully qualified name of the module in which f is defined.  If f is
        defined in the __main__ module, then the name of the file containing f
        (without its ".py" extension) is returned as the fully qualified module
        name.

    Raises:
        RuntimeError if f is defined in the __main__ module and the name of the
        file containing f does not end with ".py".
    """
    qualname = f.__module__
    if qualname == "__main__":
        qualname, ext = os.path.splitext(
            os.path.basename(f.__globals__["__file__"]))
        if ext != ".py":
            raise RuntimeError(
                f"f ({f.__qualname__}) is defined in the __main__ module but "
                f"is contained in a file ({f.__globals__['__file__']}) that "
                "does not have extension '.py'.")
    return qualname
