# Copyright 2022 Inductor, Inc.

"""Functionality for Inductor function execution common to all environments."""

import abc
from typing import Any, Dict, List


class Future(abc.ABC):
    """The result of an asynchronous call to an Inductor app function."""

    @abc.abstractmethod
    def wait(self) -> Any:
        """Blocks until the function call underlying this Future completes.

        Returns:
            The value returned by the underlying function call.

        Raises:
            Any exception raised by the underlying function call.
        """


def execute_qualname(
    module_qualname: str, fn_qualname: str,
    args: List[Any], kwargs: Dict[str, Any]) -> Any:  # pylint: disable=unused-argument
    """Executes function given by module_qualname and fn_qualname.

    Args:
        module_qualname: Fully qualified name of module containing the function
            to be executed.
        fn_qualname: Qualified name, within module given by module_qualname,
            of function to be executed.
        args: Positional arguments to be passed to function.
        kwargs: Keyword arguments to be passed to function.

    Returns:
        Value returned by function.

    Raises:
        Any exception raised by function.
    """
    if module_qualname.startswith("."):
        raise ValueError(
            "module_qualname is relative, but must be absolute "
            "(fully qualified).")
    exec_locals = locals().copy()
    exec(  # pylint: disable=exec-used
        f"import {module_qualname}; "
        f"result = {module_qualname}.{fn_qualname}(*args, **kwargs)",
        globals().copy(), exec_locals)
    return exec_locals["result"]
